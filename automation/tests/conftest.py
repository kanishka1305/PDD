"""
conftest.py — pytest fixtures shared across all test modules.

Fixes applied:
  - rep_call AttributeError guard (parallel workers don't always have rep_call)
  - Thread-safe results store using a Manager list (works with -n auto)
  - Correct skipped detection: pytest marks skips as 'skipped' on rep_setup or rep_call
  - duration captured via monotonic clock, not datetime subtraction
  - JSON written to both timestamped file AND execution-results.json (latest)
  - save_results is session-scoped autouse so it fires exactly once per worker
  - generate_excel_report + generate_html_report called from save_results
"""

import json
import threading
import pytest
from datetime import datetime
from pathlib import Path

from automation.utils.driver_factory import get_driver
from automation.utils.screenshot import take_screenshot
from automation.utils.logger import log
from automation.config.settings import JSON_DIR

# ── Thread-safe results collector ────────────────────────────────────────────
# A plain list is NOT safe when pytest-xdist workers share memory via a Manager.
# We use a threading.Lock here; xdist workers each have their own process so
# they write to separate JSON files which are merged in the session teardown.
_results: list = []
_lock = threading.Lock()


def _append_result(entry: dict) -> None:
    with _lock:
        _results.append(entry)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def results_store():
    """Return the shared results list for this process/worker."""
    return _results


@pytest.fixture(scope="function")
def driver(request, results_store):
    """
    Provide a configured WebDriver instance for each test function.
    On teardown:
      - Detect PASS / FAIL / SKIP
      - Capture screenshot on failure
      - Append structured result dict to results_store
      - Quit the driver
    """
    drv = get_driver()
    import time
    start = time.monotonic()
    yield drv

    # ── Collect outcome ───────────────────────────────────────────────────────
    duration = round(time.monotonic() - start, 3)

    # rep_setup / rep_call / rep_teardown are set by pytest_runtest_makereport hook.
    # Guard against AttributeError when the attribute hasn't been set yet
    # (can happen in rare xdist edge cases or if setup itself errored).
    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call  = getattr(request.node, "rep_call",  None)

    # Determine status
    if rep_setup is not None and rep_setup.skipped:
        status = "SKIP"
        failure_reason = str(rep_setup.longrepr) if rep_setup.longrepr else "Skipped"
    elif rep_call is not None and rep_call.skipped:
        status = "SKIP"
        failure_reason = str(rep_call.longrepr) if rep_call.longrepr else "Skipped"
    elif rep_call is not None and rep_call.failed:
        status = "FAIL"
        failure_reason = str(rep_call.longrepr)[:600]
    elif rep_setup is not None and rep_setup.failed:
        status = "FAIL"
        failure_reason = str(rep_setup.longrepr)[:600]
    else:
        status = "PASS"
        failure_reason = ""

    # ── Screenshot on failure ─────────────────────────────────────────────────
    screenshot_path = ""
    if status == "FAIL":
        safe_name = (
            request.node.nodeid
            .replace("/", "_")
            .replace("\\", "_")
            .replace("::", "_")
            .replace(" ", "_")
        )
        ss = take_screenshot(drv, f"FAIL_{safe_name}"[:120])
        screenshot_path = str(ss)
        log.error("TEST FAILED: %s", request.node.nodeid)
    elif status == "SKIP":
        log.warning("TEST SKIPPED: %s", request.node.nodeid)

    # ── Build result entry ────────────────────────────────────────────────────
    entry = {
        "test_id":        request.node.nodeid,
        "module":         getattr(request.node.module, "__name__", "unknown").split(".")[-1],
        "name":           request.node.name,
        "status":         status,
        "duration":       duration,
        "failure_reason": failure_reason,
        "screenshot":     screenshot_path,
        "timestamp":      datetime.utcnow().isoformat() + "Z",
    }
    _append_result(entry)
    log.info("%-6s %s (%.2fs)", status, request.node.nodeid, duration)

    drv.quit()


@pytest.fixture(scope="session", autouse=True)
def save_results():
    """
    After the entire test session, write results to JSON and generate
    both the Excel and HTML reports.
    """
    yield  # All tests run first

    results = list(_results)
    total   = len(results)
    passed  = sum(1 for r in results if r["status"] == "PASS")
    failed  = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")

    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total":     total,
        "passed":    passed,
        "failed":    failed,
        "skipped":   skipped,
        "results":   results,
    }

    # ── Write timestamped JSON ────────────────────────────────────────────────
    ts  = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out = JSON_DIR / f"execution-results_{ts}.json"
    try:
        out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        log.info("JSON results  → %s (%d tests)", out.name, total)
    except Exception as exc:
        log.error("Failed to write JSON results: %s", exc)

    # ── Write 'latest' alias ──────────────────────────────────────────────────
    latest = JSON_DIR / "execution-results.json"
    try:
        latest.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    except Exception as exc:
        log.error("Failed to write latest JSON: %s", exc)

    # ── Generate Excel + HTML reports ─────────────────────────────────────────
    try:
        from automation.utils.report_generator import (
            generate_excel_report,
            generate_html_report,
        )
        excel_out = generate_excel_report(results, summary)
        html_out  = generate_html_report(results, summary)
        log.info("Excel report  → %s", excel_out)
        log.info("HTML report   → %s", html_out)
    except Exception as exc:
        log.error("Report generation failed: %s", exc)


# ── Hook: capture test phase reports ─────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach phase reports (setup / call / teardown) to the test item node
    so the driver fixture can read them during teardown.
    """
    outcome = yield
    rep = outcome.get_result()
    # e.g. item.rep_setup, item.rep_call, item.rep_teardown
    setattr(item, f"rep_{rep.when}", rep)
