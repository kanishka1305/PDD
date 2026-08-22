"""
DentAI Appium — Results Page Object
======================================
Locators verified against:  DentAI-Mobile/src/screens/ResultsScreen.tsx

UI elements:
  - "Results" header title
  - Scan selector chips (e.g. "#1", "#2")
  - "Patient Information" section with InfoCells:
      Patient Name, Modality, Scan ID, Status
  - "Segmented Regions" card header + subtitle
  - Region cards: CHL, CHR, CNL, CNR, ARL, ARR, FULL
    - Short code text (e.g. "CHL")
    - Region label (e.g. "Condylar Head L")
    - "STL" button
    - "DCM" button
  - "Full Mandible Export" card header
  - "Download Full STL" button
  - "Download Full DICOM" button
  - "No analysis results yet" empty state
  - "Analyse This Scan" button (when no results)
  - "Analysed" / "Pending" badge
"""

import logging

from appium.webdriver.common.appiumby import AppiumBy

from appium.pages.base_page import BasePage
from appium.utils.test_data import UIText

logger = logging.getLogger(__name__)


class ResultsPage(BasePage):
    """Page object for the DentAI Mobile Results screen."""

    # All region short codes from ResultsScreen.tsx REGIONS array
    REGION_SHORTS = ["CHL", "CHR", "CNL", "CNR", "ARL", "ARR", "FULL"]

    # ── Verifications ──────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return self.is_text_visible(UIText.RESULTS_TITLE, timeout=15)

    def wait_for_results_screen(self, timeout: int = 15) -> bool:
        try:
            self.wait_for_text(UIText.RESULTS_TITLE, timeout=timeout)
            return True
        except Exception:
            return False

    def is_patient_info_visible(self) -> bool:
        return self.is_text_visible(UIText.PATIENT_INFO_SECTION)

    def is_analysed_badge_visible(self) -> bool:
        return self.is_text_visible("Analysed")

    def is_pending_badge_visible(self) -> bool:
        return self.is_text_visible("Pending")

    def is_segmented_regions_visible(self) -> bool:
        return self.is_text_visible(UIText.SEGMENTED_REGIONS, timeout=10)

    def is_region_card_visible(self, short_code: str) -> bool:
        """Check if a region card with the given short code is visible."""
        return self.is_text_visible(short_code, timeout=5)

    def are_all_regions_visible(self) -> bool:
        """Check all 7 region cards are rendered."""
        return all(
            self.is_region_card_visible(code) for code in self.REGION_SHORTS
        )

    def is_full_mandible_export_visible(self) -> bool:
        return self.is_text_visible(UIText.FULL_MANDIBLE_EXPORT, timeout=5)

    def is_stl_button_visible(self) -> bool:
        """Check at least one STL button is present."""
        return self.is_text_visible("STL", timeout=5)

    def is_dcm_button_visible(self) -> bool:
        return self.is_text_visible("DCM", timeout=5)

    def is_empty_state_visible(self) -> bool:
        return self.is_text_contains_visible("No analysis results", timeout=5)

    def is_analyse_this_scan_visible(self) -> bool:
        return self.is_text_visible(UIText.ANALYSE_THIS_SCAN, timeout=5)

    def get_patient_name(self) -> str:
        """Return the Patient Name cell value if visible."""
        try:
            # Patient Name label is just above its value
            # The InfoCell renders label above value — find by getting text near "N/A" or actual name
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Patient Name")',
            )
            return el.text
        except Exception:
            return ""

    def get_scan_status(self) -> str:
        """Return 'Analysed' or 'Pending' from the badge."""
        if self.is_analysed_badge_visible():
            return "Analysed"
        if self.is_pending_badge_visible():
            return "Pending"
        return "Unknown"

    # ── Actions ────────────────────────────────────────────────────────────────

    def tap_region_stl(self, region_label: str = "Full Mandible") -> None:
        """Tap the STL download button for a specific region."""
        logger.info("Tapping STL for region: %s", region_label)
        # Scroll to the region card first
        self.scroll_to_text(region_label)
        # Then tap STL — use first visible STL button if label not specific enough
        try:
            self.tap_text("STL")
        except Exception:
            logger.warning("STL button not tappable for region: %s", region_label)

    def tap_region_dcm(self, region_label: str = "Full Mandible") -> None:
        """Tap the DCM download button for a specific region."""
        logger.info("Tapping DCM for region: %s", region_label)
        self.scroll_to_text(region_label)
        try:
            self.tap_text("DCM")
        except Exception:
            logger.warning("DCM button not tappable for region: %s", region_label)

    def tap_download_full_stl(self) -> None:
        logger.info("Tapping Download Full STL")
        self.scroll_to_text(UIText.DOWNLOAD_FULL_STL)
        self.tap_text(UIText.DOWNLOAD_FULL_STL)

    def tap_download_full_dicom(self) -> None:
        logger.info("Tapping Download Full DICOM")
        self.scroll_to_text(UIText.DOWNLOAD_FULL_DICOM)
        self.tap_text(UIText.DOWNLOAD_FULL_DICOM)

    def tap_analyse_this_scan(self) -> None:
        logger.info("Tapping Analyse This Scan")
        self.tap_text(UIText.ANALYSE_THIS_SCAN)

    def select_scan_chip(self, scan_number: int) -> None:
        """Tap a scan selector chip by scan ID number."""
        logger.info("Selecting scan chip: #%d", scan_number)
        try:
            self.tap_text(f"#{scan_number}")
        except Exception:
            logger.warning("Scan chip #%d not found", scan_number)

    # ── Navigation ─────────────────────────────────────────────────────────────

    def tap_tab_upload(self) -> None:
        self.tap_text(UIText.TAB_UPLOAD)

    def tap_tab_home(self) -> None:
        self.tap_text(UIText.TAB_HOME)
