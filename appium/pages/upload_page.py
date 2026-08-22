"""
DentAI Appium — Upload Page Object
=====================================
Locators verified against:  DentAI-Mobile/src/screens/UploadScreen.tsx

UI elements:
  - "Upload Scan" header title
  - "Import DICOM, NIfTI or ZIP for AI segmentation" subtitle
  - Step indicators: "Select File", "Verify Info", "Upload", "AI Analysis"
  - Drop zone: "Tap to select a scan file"
  - Format badges: ".dcm", ".nii", ".nii.gz", ".zip"
  - "Upload Scan" button  (step 1)
  - Upload progress bar + percentage text
  - "Scan Metadata" card header (step 3)
  - "Uploaded" badge
  - MetaRow labels: Scan ID, Patient Name, Patient ID, Modality, Dimensions
  - "Run AI Segmentation" button
  - "Upload Another" button (outline)
  - "Running AI segmentation…" activity indicator text
  - Error alert text
"""

import logging
import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from appium.pages.base_page import BasePage
from appium.utils.test_data import UIText
from appium.config.config import EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class UploadPage(BasePage):
    """Page object for the DentAI Mobile Upload screen."""

    # ── Verifications ──────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return (
            self.is_text_visible(UIText.UPLOAD_TITLE)
            and self.is_text_visible(UIText.DROP_ZONE_HINT, timeout=10)
        )

    def is_step_select_file_active(self) -> bool:
        return self.is_text_visible(UIText.STEP_SELECT_FILE)

    def is_step_verify_info_active(self) -> bool:
        return self.is_text_visible(UIText.STEP_VERIFY_INFO)

    def is_step_upload_active(self) -> bool:
        return self.is_text_visible(UIText.STEP_UPLOAD)

    def is_step_ai_analysis_active(self) -> bool:
        return self.is_text_visible(UIText.STEP_AI_ANALYSIS)

    def is_all_steps_visible(self) -> bool:
        return (
            self.is_step_select_file_active()
            and self.is_step_verify_info_active()
            and self.is_step_upload_active()
            and self.is_step_ai_analysis_active()
        )

    def get_error_message(self) -> str:
        for frag in ("Unsupported format", "Upload failed", "Upload error", "empty"):
            try:
                el = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{frag}")',
                )
                return el.text
            except Exception:
                continue
        return ""

    def is_upload_complete_visible(self) -> bool:
        """Return True when 'Upload complete!' text appears."""
        return self.is_text_contains_visible("Upload complete", timeout=90)

    def is_metadata_card_visible(self) -> bool:
        return self.is_text_visible("Scan Metadata", timeout=10)

    def is_uploaded_badge_visible(self) -> bool:
        return self.is_text_visible("Uploaded", timeout=10)

    def is_run_segmentation_visible(self) -> bool:
        return self.is_text_visible(UIText.RUN_SEGMENTATION_BTN, timeout=10)

    def is_segmentation_running(self) -> bool:
        return self.is_text_contains_visible("Running AI", timeout=5)

    def get_upload_progress_text(self) -> str:
        try:
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("%")',
            )
            return el.text
        except Exception:
            return ""

    def get_metadata_scan_id(self) -> str:
        """Read Scan ID from the metadata card (format: '#123')."""
        try:
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("#")',
            )
            return el.text
        except Exception:
            return ""

    def get_file_type_badge(self) -> str:
        """Return detected file type text (DICOM / NIfTI / etc.)."""
        for ftype in ("DICOM", "NIfTI GZ", "NIfTI", "ZIP"):
            if self.is_text_contains_visible(ftype, timeout=2):
                return ftype
        return ""

    # ── Format badge validation ────────────────────────────────────────────────

    def are_format_badges_visible(self) -> bool:
        return (
            self.is_text_visible(".dcm")
            and self.is_text_visible(".nii")
            and self.is_text_visible(".zip")
        )

    # ── Actions ────────────────────────────────────────────────────────────────

    def tap_drop_zone(self) -> None:
        """
        Tap the drop zone to open the file picker.
        Note: In CI this will open the Android file picker UI.
        """
        logger.info("Tapping drop zone to open file picker")
        self.tap_text(UIText.DROP_ZONE_HINT)

    def tap_upload_scan_button(self) -> None:
        """Tap 'Upload Scan' button (step 1 → step 2)."""
        logger.info("Tapping Upload Scan button")
        self.tap_text(UIText.UPLOAD_SCAN_BTN)

    def tap_run_segmentation(self) -> None:
        """Tap 'Run AI Segmentation' button (step 3)."""
        logger.info("Tapping Run AI Segmentation")
        self.scroll_to_text(UIText.RUN_SEGMENTATION_BTN)
        self.tap_text(UIText.RUN_SEGMENTATION_BTN)

    def tap_upload_another(self) -> None:
        """Tap 'Upload Another' outline button to reset the form."""
        logger.info("Tapping Upload Another")
        self.tap_text(UIText.UPLOAD_ANOTHER_BTN)

    def wait_for_upload_complete(self, timeout: int = 120) -> bool:
        """Wait for upload progress to reach 100% / 'Upload complete!'."""
        logger.info("Waiting for upload to complete (timeout=%ds)", timeout)
        try:
            self.wait_for_text_contains("Upload complete", timeout=timeout)
            return True
        except Exception:
            # Fallback: check for metadata card appearing
            return self.is_metadata_card_visible()

    def wait_for_metadata_card(self, timeout: int = 30) -> bool:
        try:
            self.wait_for_text("Scan Metadata", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_segmentation_to_start(self, timeout: int = 15) -> bool:
        """Wait until the 'Running AI segmentation…' indicator appears."""
        try:
            self.wait_for_text_contains("Running AI", timeout=timeout)
            return True
        except Exception:
            return self.is_text_contains_visible("segmentation", timeout=3)

    def push_test_file_to_device(self, local_path: str, device_path: str) -> None:
        """
        Push a local test file to the Android device for use in upload tests.
        Equivalent to `adb push`.
        """
        logger.info("Pushing %s → %s", local_path, device_path)
        try:
            self.driver.push_file(device_path, source_path=local_path)
        except Exception as exc:
            logger.error("push_file failed: %s", exc)
            raise
