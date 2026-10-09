"""
DentAI Mobile — Home / Dashboard Tests
=======================================
TC-APP-005  Home Screen Verification
"""

import pytest

from appium_tests.pages.home_page import HomePage
from appium_tests.utils.test_data import UIText


class TestHome:
    """Home — Dashboard screen test cases."""

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.tc_id("TC-APP-005")
    @pytest.mark.module("Home")
    @pytest.mark.precond("User is logged in and Dashboard is visible")
    @pytest.mark.steps(
        "1. Login with valid credentials\n"
        "2. Verify 'Good day, Dr.' greeting is present\n"
        "3. Verify 'Clinical overview' subtitle\n"
        "4. Verify all 4 KPI cards: Patients, Total Scans, Analysed, Pending\n"
        "5. Verify Quick Actions section: Upload Scan, View History, Open Results\n"
        "6. Scroll down\n"
        "7. Verify 'Recent Activity' section\n"
        "8. Verify 'System Status' section with Backend API row"
    )
    @pytest.mark.expected(
        "All dashboard sections visible: KPIs, Quick Actions, Recent Activity, System Status"
    )
    def test_home_screen_all_elements_visible(self, authenticated_driver):
        """
        TC-APP-005 — Home Screen Verification

        After login, verify every section of the Dashboard screen is displayed.
        """
        home = HomePage(authenticated_driver)

        # ── Greeting ──────────────────────────────────────────────────────────
        assert home.is_loaded(), (
            "Dashboard not loaded — 'Good day' greeting or 'Clinical overview' not visible"
        )
        greeting = home.get_greeting_text()
        assert "Good day" in greeting, (
            f"Expected greeting to contain 'Good day', got: '{greeting}'"
        )

        # ── KPI Cards ────────────────────────────────────────────────────────
        home.wait_for_scans_loaded()
        assert home.is_kpi_patients_visible(), "'Patients' KPI card not visible"
        assert home.is_kpi_scans_visible(),    "'Total Scans' KPI card not visible"
        assert home.is_kpi_analysed_visible(), "'Analysed' KPI card not visible"
        assert home.is_kpi_pending_visible(),  "'Pending' KPI card not visible"
        home.take_screenshot("TC_APP_005_kpi_cards")

        # ── Quick Actions ────────────────────────────────────────────────────
        assert home.is_quick_actions_visible(), (
            "Quick Actions section not fully visible "
            "(expected: Upload Scan, View History, Open Results)"
        )
        home.take_screenshot("TC_APP_005_quick_actions")

        # ── Recent Activity ───────────────────────────────────────────────────
        home.scroll_down()
        home.short_sleep(1)
        assert home.is_recent_activity_visible(), (
            "'Recent Activity' section not visible after scrolling"
        )

        # ── System Status ─────────────────────────────────────────────────────
        home.scroll_down()
        home.short_sleep(1)
        assert home.is_system_status_visible(), (
            "'System Status' section not visible"
        )
        assert home.is_backend_status_visible(), (
            "'Backend API' row not visible in System Status"
        )
        home.take_screenshot("TC_APP_005_system_status")

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.tc_id("TC-APP-005b")
    @pytest.mark.module("Home")
    @pytest.mark.precond("User is logged in and on Dashboard")
    @pytest.mark.steps(
        "1. Pull down to refresh the dashboard\n"
        "2. Wait for data to reload\n"
        "3. Verify dashboard elements still visible after refresh"
    )
    @pytest.mark.expected("Dashboard refreshes and all elements remain visible")
    def test_home_screen_pull_to_refresh(self, authenticated_driver):
        """
        TC-APP-005b — Dashboard Pull-to-Refresh

        Verify that pull-to-refresh reloads data without breaking the UI.
        """
        home = HomePage(authenticated_driver)
        assert home.is_loaded(), "Dashboard not visible before pull-to-refresh"

        # Scroll back to top first
        home.scroll_up()
        home.short_sleep(0.5)

        # Pull to refresh
        home.pull_to_refresh()

        # Verify dashboard still intact after refresh
        assert home.is_loaded(), (
            "Dashboard broken after pull-to-refresh"
        )
        home.take_screenshot("TC_APP_005b_pull_refresh")
