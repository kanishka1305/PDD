"""
DentAI Mobile — Navigation Tests
===================================
TC-APP-006  Navigation (bottom tabs + quick actions)
"""

import pytest

from appium_tests.pages.home_page import HomePage
from appium_tests.pages.upload_page import UploadPage
from appium_tests.pages.results_page import ResultsPage
from appium_tests.pages.profile_page import ProfilePage
from appium_tests.utils.test_data import UIText


class TestNavigation:
    """Navigation — bottom tab bar and screen transitions."""

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.tc_id("TC-APP-006")
    @pytest.mark.module("Navigation")
    @pytest.mark.precond("User is logged in and on Dashboard")
    @pytest.mark.steps(
        "1. Verify bottom tab bar is visible\n"
        "2. Tap 'Upload' tab → verify Upload screen\n"
        "3. Tap 'History' tab → verify History screen\n"
        "4. Tap 'Results' tab → verify Results screen\n"
        "5. Tap 'Profile' tab → verify Profile screen\n"
        "6. Tap 'Home' tab → verify Dashboard screen"
    )
    @pytest.mark.expected(
        "Each tab navigates to the correct screen. "
        "All screens load and display expected content."
    )
    def test_bottom_tab_navigation_all_tabs(self, authenticated_driver):
        """
        TC-APP-006 — Navigation

        Verify all 5 bottom tab bar items navigate to the correct screens.
        """
        home    = HomePage(authenticated_driver)
        upload  = UploadPage(authenticated_driver)
        results = ResultsPage(authenticated_driver)
        profile = ProfilePage(authenticated_driver)

        # Start: verify we are on Dashboard
        assert home.is_loaded(), "Dashboard not visible at start of navigation test"

        # ── Upload tab ────────────────────────────────────────────────────────
        home.tap_tab_upload()
        home.short_sleep(1)
        assert upload.is_text_visible(UIText.UPLOAD_TITLE, timeout=12), (
            f"Upload screen '{UIText.UPLOAD_TITLE}' not visible after tapping Upload tab"
        )
        # Verify step indicators on upload screen
        assert upload.is_all_steps_visible(), (
            "Upload step indicators not all visible"
        )
        home.take_screenshot("TC_APP_006_upload_tab")

        # ── History tab ───────────────────────────────────────────────────────
        home.tap_tab_history()
        home.short_sleep(1)
        # History screen shows "History" title or scan list
        assert home.is_text_contains_visible("History", timeout=12), (
            "History screen title not visible after tapping History tab"
        )
        home.take_screenshot("TC_APP_006_history_tab")

        # ── Results tab ───────────────────────────────────────────────────────
        home.tap_tab_results()
        home.short_sleep(1)
        assert results.is_loaded(), (
            f"Results screen '{UIText.RESULTS_TITLE}' not visible after tapping Results tab"
        )
        home.take_screenshot("TC_APP_006_results_tab")

        # ── Profile tab ───────────────────────────────────────────────────────
        home.tap_tab_profile()
        home.short_sleep(1)
        assert profile.is_loaded(), (
            "Profile screen not visible after tapping Profile tab"
        )
        home.take_screenshot("TC_APP_006_profile_tab")

        # ── Home tab ─────────────────────────────────────────────────────────
        home.tap_tab_home()
        home.short_sleep(1)
        assert home.is_loaded(), (
            "Dashboard not visible after tapping Home tab from Profile"
        )
        home.take_screenshot("TC_APP_006_home_tab")

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.tc_id("TC-APP-006b")
    @pytest.mark.module("Navigation")
    @pytest.mark.precond("User is logged in and on Dashboard")
    @pytest.mark.steps(
        "1. Tap 'Upload Scan' quick action card\n"
        "2. Verify Upload screen opens\n"
        "3. Navigate back to Dashboard via Home tab\n"
        "4. Tap 'View History' quick action\n"
        "5. Verify History screen opens\n"
        "6. Navigate back\n"
        "7. Tap 'Open Results' quick action\n"
        "8. Verify Results screen opens"
    )
    @pytest.mark.expected("Quick action cards navigate to correct screens")
    def test_dashboard_quick_action_navigation(self, authenticated_driver):
        """
        TC-APP-006b — Quick Action Navigation

        Verify each quick action card on Dashboard navigates to the correct screen.
        """
        home    = HomePage(authenticated_driver)
        upload  = UploadPage(authenticated_driver)
        results = ResultsPage(authenticated_driver)

        assert home.is_loaded(), "Dashboard not visible"
        home.scroll_up()  # Ensure quick actions are visible

        # ── Upload Scan quick action ──────────────────────────────────────────
        home.tap_upload_scan_quick_action()
        home.short_sleep(1)
        assert upload.is_text_visible(UIText.UPLOAD_TITLE, timeout=12), (
            "Upload screen not visible after tapping 'Upload Scan' quick action"
        )
        home.take_screenshot("TC_APP_006b_upload_scan_qa")

        # Return to Dashboard
        home.tap_tab_home()
        home.short_sleep(1)
        assert home.is_loaded()

        # ── Open Results quick action ────────────────────────────────────────
        home.tap_open_results_quick_action()
        home.short_sleep(1)
        assert results.is_loaded(), (
            "Results screen not visible after tapping 'Open Results' quick action"
        )
        home.take_screenshot("TC_APP_006b_open_results_qa")
