"""
conftest_excel.py  —  pytest plugin for per-test Excel reporting
================================================================

Hooks implemented
-----------------
pytest_sessionstart      — record session start time
pytest_runtest_setup     — record per-test start time
pytest_runtest_logreport — collect outcome for each phase (setup/call/teardown)
pytest_runtest_makereport— attach phase report to item node (tryfirst)
pytest_sessionfinish     — write individual .xlsx per test + overall_test_report.xlsx

Registration
------------
This file is imported as a plugin in automation/tests/conftest.py via:

    pytest_plugins = ["automation.plugin.conftest_excel"]

It does NOT touch or replace any existing fixture in conftest.py.

Design
------
- Each test item gets a _excel_record dict stored on the item object.
- Screenshots are captured automatically on FAIL/ERROR by reaching into
  the item's driver fixture value via request._fixture_defs (safe fallback).
- Individual reports are written immediately after each test finishes so
  partial results are available even if the session is interrupted.
- The overall report is written once at sessionfinish.
"""

from __future__ import annotations

import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Lazy import of the reporter so collection errors don't surface as ImportError
# if openpyxl isn't installed yet.  The import is deferred to sessionfinish.
# ---------------------------------------------------------------------------


def _import_reporter():
    try:
        from automation.utils.excel_reporter import (
            write_individual_report,
            write_overall_report,
            SCREENSHOTS_DIR,
        )
        return write_individual_report, write_overall_report, SCREENSHOTS_DIR
    except ImportError as exc:
        # openpyxl not installed — emit a warning but don't crash the suite
        import warnings
        warnings.warn(f"Excel reporter unavailable: {exc}", stacklevel=2)
        return None, None, None


# ---------------------------------------------------------------------------
# Module-level state (one per pytest worker process)
# ---------------------------------------------------------------------------

_SESSION_START: datetime | None = None
_SESSION_END:   datetime | None = None
_ALL_RECORDS:   list[dict]      = []   # accumulated across the whole session


# ---------------------------------------------------------------------------
# Helper — extract driver from item so we can take screenshots
# ---------------------------------------------------------------------------

def _try_screenshot(item: pytest.Item, label: str) -> str:
    """
    Attempt to capture a screenshot using the Selenium driver attached to
    the test item.  Returns the screenshot file path string, or "".

    Strategy:
      1. Look for item._request.getfixturevalue("driver")  (most reliable)
      2. Walk item._fixture_defs for a fixture named "driver"
      3. Give up gracefully — no crash, just empty string
    """
    try:
        screenshots_dir = Path(__file__).parent.parent.parent / "reports" / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        # Try to get the driver fixture value
        driver = None
        try:
            # pytest stores the resolved fixture instance on the funcargs dict
            driver = item.funcargs.get("driver")
        except AttributeError:
            pass

        if driver is None:
            return ""

        ts  = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        safe = label.replace(" ", "_").replace("::", "_").replace("/", "_")[:80]
        path = screenshots_dir / f"FAIL_{safe}_{ts}.png"
        driver.save_screenshot(str(path))
        return str(path)
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Hook: session start
# ---------------------------------------------------------------------------

def pytest_sessionstart(session: pytest.Session) -> None:
    global _SESSION_START, _ALL_RECORDS
    _SESSION_START = datetime.utcnow()
    _ALL_RECORDS   = []


# ---------------------------------------------------------------------------
# Hook: attach start time to each item before it runs
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item: pytest.Item, nextitem: Any):
    """Initialise the per-item record dict before the test protocol starts."""
    item._excel_record: dict = {
        "nodeid":          item.nodeid,
        "name":            item.name,
        "file":            str(item.fspath),
        "function":        item.name,
        "module":          item.module.__name__.split(".")[-1] if hasattr(item, "module") else "",
        "status":          "UNKNOWN",
        "start_time":      datetime.utcnow(),
        "end_time":        None,
        "duration":        0.0,
        "browser":         os.environ.get("BROWSER", "Chrome"),
        "os":              platform.system(),
        "environment":     "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") else "Local",
        "error_message":   "",
        "screenshot_path": "",
    }
    yield
    # end_time is filled in by pytest_runtest_logreport below


# ---------------------------------------------------------------------------
# Hook: collect outcome after each phase (setup / call / teardown)
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: Any):
    """
    Runs tryfirst so we can attach rep_setup / rep_call / rep_teardown to the
    item — same approach used by conftest.py for the driver fixture.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_logreport(report: pytest.TestReport):
    """
    Called after setup, call, and teardown phases.
    We only finalise the record after the *call* phase (or setup if skipped).
    """
    yield  # let other plugins run first

    # Retrieve the item — available on pytest.TestReport in modern pytest
    item = getattr(report, "item", None)

    # Fallback: in some pytest versions the item isn't on the report;
    # we handle this in pytest_runtest_protocol via the item reference below.
    if item is None:
        return

    rec: dict | None = getattr(item, "_excel_record", None)
    if rec is None:
        return

    if report.when == "call" or (report.when == "setup" and report.skipped):
        rec["end_time"] = datetime.utcnow()
        rec["duration"] = report.duration

        if report.passed:
            rec["status"] = "PASS"
        elif report.skipped:
            rec["status"] = "SKIP"
            rec["error_message"] = str(report.longrepr) if report.longrepr else "Skipped"
        elif report.failed:
            rec["status"] = "FAIL"
            longrepr = report.longreprtext if hasattr(report, "longreprtext") else str(report.longrepr or "")
            rec["error_message"] = longrepr[:800]
            # Capture screenshot
            rec["screenshot_path"] = _try_screenshot(item, item.nodeid)


# ---------------------------------------------------------------------------
# Hook: write individual report right after the full test (all 3 phases done)
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item: pytest.Item, nextitem: Any):  # noqa: F811 — re-defined intentionally
    """
    NOTE: pytest allows multiple hookwrappers for the same hook.
    The first definition (above) initialises the record.
    This second wrapper writes the individual report after the item finishes.
    """
    yield

    rec: dict | None = getattr(item, "_excel_record", None)
    if rec is None:
        return

    # Fill missing end_time (can happen if setup failed before call)
    if rec.get("end_time") is None:
        rec["end_time"] = datetime.utcnow()
        start = rec.get("start_time")
        if isinstance(start, datetime):
            rec["duration"] = (rec["end_time"] - start).total_seconds()

    # Determine final status from phase reports
    rep_setup = getattr(item, "rep_setup", None)
    rep_call  = getattr(item, "rep_call",  None)

    if rep_setup is not None and rep_setup.skipped:
        rec["status"] = "SKIP"
    elif rep_call is not None and rep_call.passed:
        rec["status"] = "PASS"
    elif rep_call is not None and rep_call.failed:
        rec["status"] = "FAIL"
        if not rec["error_message"]:
            longrepr = rep_call.longreprtext if hasattr(rep_call, "longreprtext") else str(rep_call.longrepr or "")
            rec["error_message"] = longrepr[:800]
        if not rec["screenshot_path"]:
            rec["screenshot_path"] = _try_screenshot(item, item.nodeid)
    elif rep_setup is not None and rep_setup.failed:
        rec["status"] = "ERROR"
        if not rec["error_message"]:
            longrepr = rep_setup.longreprtext if hasattr(rep_setup, "longreprtext") else str(rep_setup.longrepr or "")
            rec["error_message"] = longrepr[:800]

    # Accumulate for the overall report
    _ALL_RECORDS.append(dict(rec))

    # Write individual report — wrapped so a write failure never kills the test
    write_individual, _, _ = _import_reporter()
    if write_individual is not None:
        try:
            out = write_individual(rec)
        except Exception as exc:
            import warnings
            warnings.warn(f"Individual Excel report failed for {item.nodeid}: {exc}")


# ---------------------------------------------------------------------------
# Hook: session finish — write the overall report
# ---------------------------------------------------------------------------

def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    global _SESSION_END
    _SESSION_END = datetime.utcnow()

    if not _ALL_RECORDS:
        return

    _, write_overall, _ = _import_reporter()
    if write_overall is None:
        return

    try:
        out = write_overall(
            _ALL_RECORDS,
            _SESSION_START or datetime.utcnow(),
            _SESSION_END,
        )
        # Print a visible line in CI logs
        total   = len(_ALL_RECORDS)
        passed  = sum(1 for r in _ALL_RECORDS if r.get("status") == "PASS")
        failed  = sum(1 for r in _ALL_RECORDS if r.get("status") == "FAIL")
        skipped = sum(1 for r in _ALL_RECORDS if r.get("status") in ("SKIP", "SKIPPED"))
        print(
            f"\n[Excel Reporter] overall_test_report.xlsx → {out}\n"
            f"  Tests: {total}  PASS: {passed}  FAIL: {failed}  SKIP: {skipped}\n"
            f"  Individual reports: reports/excel/"
        )
    except Exception as exc:
        import warnings
        warnings.warn(f"Overall Excel report failed: {exc}")
