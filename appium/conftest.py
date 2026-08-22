"""
DentAI Appium — Root conftest.py
==================================
Provides:
  - Appium driver fixture (session-scoped + function-scoped)
  - Automatic screenshot on test failure
  - Test result collection
  - Excel + HTML report generation at end of session
  - Pytest hooks (runtest_makereport, sessionfinish)
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest

from appium.utils.driver_factory import create_driver, quit_driver
from appium.utils.logger import setup_logger
from appium.config.config import SCREENSHOTS_DIR
from appium.utils.test_data import DEVICE_NAME, PLATFORM_VERSION

logger = setup_logger("dentai_appium.conftest")

# ── Shared results store ───────────────────────────────────────────────────────
# Collected by pytest_runtest_makereport hook and written to Excel at session end.
_ALL_RESULTS: list[dict] = []


# ── pytest_configure ───────────────────────────────────────────────────────────
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "smoke: fast sanity checks"
    )
    config.addinivalue_line(
        "markers", "e2e: full end-to-end workflow"
    )
    config.addinivalue_line(
        "markers", "slow: long-running tests (AI segmentation wait)"
    )


# ── Shared driver fixture (function scope) ─────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    """
    Create a fresh Appium driver for each test function.
    Quits the driver after the test completes (pass or fail).
    """
    logger.info("=" * 60)
    logger.info("Starting Appium driver session")
    d = None
    try:
        d = create_driver(install_app=True)
        # Allow the React Native app to fully initialise
        time.sleep(3)
        yield d
    except Exception as exc:
        logger.error("Driver creation failed: %s", exc)
        pytest.skip(f"Appium driver unavailable: {exc}")
    finally:
        logger.info("Quitting Appium driver session")
        quit_driver(d)


# ── Pre-authenticated driver ───────────────────────────────────────────────────
@pytest.fixture(scope="function")
def authenticated_driver(driver):
    """
    Driver fixture that performs login before yielding.
    Use for tests that require an authenticated session.
    """
    from appium.pages.login_page import LoginPage
    from appium.pages.home_page import HomePage
    from appium.utils.test_data import VALID_EMAIL, VALID_PASSWORD

    login_page = LoginPage(driver)
    home_page  = HomePage(driver)

    # Wait for login screen
    if not login_page.wait_for_login_screen(timeout=20):
        # App may already be on dashboard (if APK state persists)
        if home_page.is_text_visible("Good day", timeout=5):
            logger.info("Already authenticated — skipping login")
            yield driver
            return
        pytest.skip("Login screen not reachable — skipping authenticated test")
        return

    login_page.login(VALID_EMAIL, VALID_PASSWORD)

    # Wait for dashboard
    if not home_page.wait_for_dashboard(timeout=20):
        # Capture screenshot of failure state
        login_page.take_screenshot("auth_driver_login_failed")
        pytest.skip("Login did not succeed — backend may be unreachable")
        return

    logger.info("Pre-login complete — yielding authenticated driver")
    yield driver


# ── pytest_runtest_makereport ──────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After each test phase:
      1. Capture screenshot if the test FAILED.
      2. Collect result metadata for the Excel report.
    """
    outcome = yield
    report  = outcome.get_result()

    # Only process the "call" phase (not setup/teardown)
    if report.when != "call":
        return

    status = "PASS" if report.passed else ("SKIP" if report.skipped else "FAIL")

    # ── Screenshot on failure ──────────────────────────────────────────────────
    screenshot_path = ""
    if report.failed:
        d = item.funcargs.get("driver") or item.funcargs.get("authenticated_driver")
        if d:
            try:
                ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
                fname = f"FAIL_{item.name}_{ts}.png"
                path  = SCREENSHOTS_DIR / fname
                d.save_screenshot(str(path))
                screenshot_path = str(path)
                logger.info("Failure screenshot → %s", path)

                # Attach to pytest HTML report if plugin available
                try:
                    from pytest_html import extras
                    item._html_extras = getattr(item, "_html_extras", [])
                    item._html_extras.append(
                        extras.image(screenshot_path, name="Failure Screenshot")
                    )
                except Exception:
                    pass
            except Exception as exc:
                logger.warning("Screenshot capture failed: %s", exc)

    # ── Collect test result ────────────────────────────────────────────────────
    # Extract metadata from test item markers / docstring
    tc_id     = _get_marker_value(item, "tc_id",     item.name)
    module    = _get_marker_value(item, "module",    _infer_module(item))
    precond   = _get_marker_value(item, "precond",   "App launched and accessible")
    steps     = _get_marker_value(item, "steps",     item.function.__doc__ or "")
    expected  = _get_marker_value(item, "expected",  "Test passes without errors")

    error_msg = ""
    if report.failed:
        error_msg = _extract_error(report)

    duration = getattr(report, "duration", 0.0)

    _ALL_RESULTS.append({
        "tc_id":       tc_id,
        "name":        item.name,
        "module":      module,
        "status":      status,
        "start_time":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_time":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration":    duration,
        "error":       error_msg,
        "screenshot":  screenshot_path,
        "precondition": precond,
        "steps":       steps[:500],
        "expected":    expected,
        "actual":      "PASSED" if status == "PASS" else error_msg[:200],
    })


# ── pytest_sessionfinish ───────────────────────────────────────────────────────
def pytest_sessionfinish(session, exitstatus):
    """Generate Excel + HTML reports after all tests complete."""
    if not _ALL_RESULTS:
        logger.info("No test results collected — skipping report generation.")
        return

    try:
        from appium.utils.excel_report import generate_reports
        excel_path, html_path = generate_reports(_ALL_RESULTS)
        print(f"\n{'='*60}")
        print(f"  APPIUM E2E REPORT GENERATED")
        print(f"{'='*60}")
        print(f"  Excel → {excel_path}")
        print(f"  HTML  → {html_path}")

        # Print summary to console
        total   = len(_ALL_RESULTS)
        passed  = sum(1 for r in _ALL_RESULTS if r["status"] == "PASS")
        failed  = sum(1 for r in _ALL_RESULTS if r["status"] == "FAIL")
        skipped = sum(1 for r in _ALL_RESULTS if r["status"] == "SKIP")
        rate    = passed / max(total, 1) * 100

        print(f"\n  Total: {total} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
        print(f"  Pass Rate: {rate:.1f}%")
        print(f"  Device: {DEVICE_NAME} | Android {PLATFORM_VERSION}")
        print(f"{'='*60}\n")

    except Exception as exc:
        logger.error("Report generation failed: %s", exc)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_marker_value(item, marker_name: str, default: str) -> str:
    m = item.get_closest_marker(marker_name)
    if m and m.args:
        return str(m.args[0])
    return default


def _infer_module(item) -> str:
    """Infer module from the test file name."""
    file_name = Path(item.fspath).stem  # e.g. "test_login"
    return file_name.replace("test_", "").replace("_", " ").title()


def _extract_error(report) -> str:
    """Extract a clean error message from the report."""
    if report.longrepr:
        text = str(report.longrepr)
        # Take only the last AssertionError line
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for line in reversed(lines):
            if line.startswith("AssertionError") or line.startswith("E "):
                return line[:300]
        return lines[-1][:300] if lines else "Unknown error"
    return ""
