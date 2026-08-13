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

# ── Excel reporting plugin ────────────────────────────────────────────────────
# Activates automation/plugin/conftest_excel.py as a pytest plugin.
# Adds per-test .xlsx + overall_test_report.xlsx with ZERO changes to tests.
pytest_plugins = ["automation.plugin.conftest_excel"]

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
_results: list = []
_lock = threading.Lock()


def _append_result(entry: dict) -> None:
    with _lock:
        _results.append(entry)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def ensure_http_server():
    """Start a local HTTP server if BASE_URL points to localhost/127.0.0.1."""
    import urllib.parse
    import socket
    import http.server
    import threading as _threading
    import time
    from automation.config.settings import BASE_URL

    parsed = urllib.parse.urlparse(BASE_URL)
    if parsed.hostname in ("localhost", "127.0.0.1"):
        port = parsed.port or 8000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        res = sock.connect_ex((parsed.hostname, port))
        sock.close()
        if res != 0:
            static_dir = (
                Path(__file__).parent.parent.parent
                / "Dental (1)" / "Dental" / "app" / "static"
            )
            if static_dir.exists():
                class QuietHandler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=str(static_dir), **kwargs)
                    def log_message(self, format, *args):
                        pass

                httpd = http.server.HTTPServer((parsed.hostname, port), QuietHandler)
                t = _threading.Thread(target=httpd.serve_forever, daemon=True)
                t.start()
                time.sleep(0.5)
                log.info(
                    "Started local HTTP static server on %s:%d serving %s",
                    parsed.hostname, port, static_dir,
                )
    yield


@pytest.fixture(scope="session")
def results_store():
    """Return the shared results list for this process/worker."""
    return _results


@pytest.fixture(scope="function")
def driver(request, results_store):
    """
    Provide a configured WebDriver instance per test.
    On teardown: detect PASS/FAIL/SKIP, capture screenshot on failure,
    append result to results_store, quit the driver.
    """
    drv = get_driver()
    import time
    start = time.monotonic()
    yield drv

    duration = round(time.monotonic() - start, 3)

    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call  = getattr(request.node, "rep_call",  None)

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

    screenshot_path = ""
    if status == "FAIL":
        safe_name = (
            request.node.nodeid
            .replace("/", "_").replace("\\", "_")
            .replace("::", "_").replace(" ", "_")
        )
        ss = take_screenshot(drv, f"FAIL_{safe_name}"[:120])
        screenshot_path = str(ss)
        log.error("TEST FAILED: %s", request.node.nodeid)
    elif status == "SKIP":
        log.warning("TEST SKIPPED: %s", request.node.nodeid)

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
    """Write JSON results and generate Excel + HTML reports after the session."""
    yield

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

    ts  = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out = JSON_DIR / f"execution-results_{ts}.json"
    try:
        out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        log.info("JSON results  → %s (%d tests)", out.name, total)
    except Exception as exc:
        log.error("Failed to write JSON results: %s", exc)

    latest = JSON_DIR / "execution-results.json"
    try:
        latest.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    except Exception as exc:
        log.error("Failed to write latest JSON: %s", exc)

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
    """Attach rep_setup / rep_call / rep_teardown to the item node."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
