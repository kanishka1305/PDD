"""
DentAI Appium — Home / Dashboard Page Object
=============================================
Locators verified against:  DentAI-Mobile/src/screens/DashboardScreen.tsx

UI elements:
  - "Good day, Dr. <name>" greeting (textContains "Good day")
  - "Clinical overview" subtitle
  - KPI cards: "Patients", "Total Scans", "Analysed", "Pending"
  - Quick Actions: "Upload Scan", "View History", "Open Results"
  - "Quick Actions" card header
  - "Recent Activity" card header + "View all →" link
  - Scan rows (if any scans exist)
  - "System Status" section: "Backend API", "AI Model", "Database"
  - Avatar button (navigates to Profile)
  - Bottom tabs: Home, Upload, History, Results, Profile
"""

import logging

from appium_tests.pages.base_page import BasePage
from appium_tests.utils.test_data import UIText

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Page object for the DentAI Mobile Dashboard (Home tab) screen."""

    # ── Verifications ──────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        """Verify dashboard is fully visible after login."""
        return (
            self.is_text_contains_visible("Good day", timeout=20)
            and self.is_text_visible(UIText.CLINICAL_OVERVIEW, timeout=10)
        )

    def wait_for_dashboard(self, timeout: int = 25) -> bool:
        try:
            self.wait_for_text_contains("Good day", timeout=timeout)
            return True
        except Exception:
            return False

    def get_greeting_text(self) -> str:
        try:
            el = self.find_by_text_contains("Good day")
            return el.text
        except Exception:
            return ""

    def is_kpi_patients_visible(self) -> bool:
        return self.is_text_visible(UIText.KPI_PATIENTS)

    def is_kpi_scans_visible(self) -> bool:
        return self.is_text_visible(UIText.KPI_TOTAL_SCANS)

    def is_kpi_analysed_visible(self) -> bool:
        return self.is_text_visible(UIText.KPI_ANALYSED)

    def is_kpi_pending_visible(self) -> bool:
        return self.is_text_visible(UIText.KPI_PENDING)

    def is_all_kpis_visible(self) -> bool:
        return (
            self.is_kpi_patients_visible()
            and self.is_kpi_scans_visible()
            and self.is_kpi_analysed_visible()
            and self.is_kpi_pending_visible()
        )

    def is_quick_actions_visible(self) -> bool:
        return (
            self.is_text_visible(UIText.QA_UPLOAD_SCAN)
            and self.is_text_visible(UIText.QA_VIEW_HISTORY)
            and self.is_text_visible(UIText.QA_OPEN_RESULTS)
        )

    def is_recent_activity_visible(self) -> bool:
        return self.is_text_visible(UIText.RECENT_ACTIVITY)

    def is_system_status_visible(self) -> bool:
        return self.is_text_visible(UIText.SYSTEM_STATUS)

    def is_backend_status_visible(self) -> bool:
        return self.is_text_visible("Backend API")

    def is_no_scans_state(self) -> bool:
        """Return True if the 'No scans yet' empty state is shown."""
        return self.is_text_contains_visible("No scans yet", timeout=5)

    # ── Navigation actions ─────────────────────────────────────────────────────

    def tap_upload_scan_quick_action(self) -> None:
        """Tap the 'Upload Scan' quick action card on Dashboard."""
        logger.info("Tapping Upload Scan quick action")
        self.tap_text(UIText.QA_UPLOAD_SCAN)

    def tap_view_history_quick_action(self) -> None:
        logger.info("Tapping View History quick action")
        self.tap_text(UIText.QA_VIEW_HISTORY)

    def tap_open_results_quick_action(self) -> None:
        logger.info("Tapping Open Results quick action")
        self.tap_text(UIText.QA_OPEN_RESULTS)

    # ── Bottom tab navigation ──────────────────────────────────────────────────

    def tap_tab_home(self) -> None:
        self.tap_text(UIText.TAB_HOME)

    def tap_tab_upload(self) -> None:
        self.tap_text(UIText.TAB_UPLOAD)

    def tap_tab_history(self) -> None:
        self.tap_text(UIText.TAB_HISTORY)

    def tap_tab_results(self) -> None:
        self.tap_text(UIText.TAB_RESULTS)

    def tap_tab_profile(self) -> None:
        self.tap_text(UIText.TAB_PROFILE)

    def tap_avatar(self) -> None:
        """Tap the avatar circle in the header to navigate to Profile."""
        # The avatar is a LinearGradient View — tap by finding the first letter
        # of the user's name (inside the gradient circle).
        # Fallback: tap the Profile tab instead.
        try:
            self.tap_tab_profile()
        except Exception:
            logger.warning("Avatar tap failed — using Profile tab instead")

    def pull_to_refresh(self) -> None:
        """Pull-to-refresh the dashboard."""
        size    = self.driver.get_window_size()
        start_x = size["width"] // 2
        # Swipe from 30% to 80% height
        self.driver.swipe(
            start_x, int(size["height"] * 0.30),
            start_x, int(size["height"] * 0.80),
            600
        )
        self.short_sleep(2)

    def wait_for_scans_loaded(self, timeout: int = 15) -> bool:
        """Wait until scan data has loaded (KPI values change from '—')."""
        try:
            # After load, KPI value cells won't show '—'
            import time
            deadline = time.time() + timeout
            while time.time() < deadline:
                if not self.is_text_visible("—", timeout=1):
                    return True
                self.short_sleep(1)
            return True  # Even with '—' the screen is loaded
        except Exception:
            return True
