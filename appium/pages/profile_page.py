"""
DentAI Appium — Profile Page Object (includes Logout)
=======================================================
Locators verified against:  DentAI-Mobile/src/screens/ProfileScreen.tsx

UI elements:
  - Header: "Dr. <name>" (textContains "Dr.")
  - User email text
  - "Personal Information" card
  - Full Name EditText    [1]
  - Email EditText        [2]  (disabled/readonly)
  - Phone Number EditText [3]
  - Clinic / Hospital     [4]
  - "Save Changes" button
  - "Security" section:
    - "🔒  Change Password" menu item
    - "🎓  My Credentials" menu item
  - "About" section: Version 1.0.0, Backend, AI Model
  - "Sign Out" button (danger / red)
  - Alert dialog: "Sign Out" title
    - "Cancel" button
    - "Sign Out" (confirm) button
"""

import logging
import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from appium.pages.base_page import BasePage
from appium.utils.test_data import UIText

logger = logging.getLogger(__name__)


class ProfilePage(BasePage):
    """Page object for the DentAI Mobile Profile screen."""

    # ── Verifications ──────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return (
            self.is_text_contains_visible("Dr.", timeout=15)
            and self.is_text_visible(UIText.PERSONAL_INFO, timeout=10)
        )

    def wait_for_profile_screen(self, timeout: int = 15) -> bool:
        try:
            self.wait_for_text(UIText.PERSONAL_INFO, timeout=timeout)
            return True
        except Exception:
            return False

    def get_user_name_text(self) -> str:
        try:
            el = self.find_by_text_contains("Dr.")
            return el.text
        except Exception:
            return ""

    def get_user_email_text(self) -> str:
        """Return the email text displayed under the user name."""
        try:
            # Email is shown as plain text in the profile header
            els = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("@")',
            )
            return els[0].text if els else ""
        except Exception:
            return ""

    def get_success_message(self) -> str:
        try:
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("updated successfully")',
            )
            return el.text
        except Exception:
            return ""

    def get_error_message(self) -> str:
        try:
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Cannot reach")',
            )
            return el.text
        except Exception:
            return ""

    def is_save_changes_visible(self) -> bool:
        return self.is_text_visible(UIText.SAVE_CHANGES_BTN)

    def is_sign_out_visible(self) -> bool:
        return self.is_text_visible(UIText.SIGN_OUT_BTN)

    def is_about_section_visible(self) -> bool:
        return self.is_text_visible("About") and self.is_text_visible("1.0.0")

    def is_version_visible(self) -> bool:
        return self.is_text_visible("1.0.0")

    # ── Actions ────────────────────────────────────────────────────────────────

    def enter_full_name(self, name: str) -> "ProfilePage":
        logger.info("Updating full name: %s", name)
        self.type_into_field(1, name)
        return self

    def enter_phone(self, phone: str) -> "ProfilePage":
        logger.info("Updating phone: %s", phone)
        self.type_into_field(3, phone)
        return self

    def enter_clinic(self, clinic: str) -> "ProfilePage":
        logger.info("Updating clinic: %s", clinic)
        self.type_into_field(4, clinic)
        return self

    def tap_save_changes(self) -> None:
        logger.info("Tapping Save Changes")
        self.hide_keyboard()
        self.scroll_to_text(UIText.SAVE_CHANGES_BTN)
        self.tap_text(UIText.SAVE_CHANGES_BTN)

    def tap_change_password(self) -> None:
        self.tap_text("🔒  Change Password")

    def tap_my_credentials(self) -> None:
        self.tap_text("🎓  My Credentials")

    def tap_sign_out(self) -> None:
        """Tap the 'Sign Out' danger button — opens confirmation dialog."""
        logger.info("Tapping Sign Out button")
        self.scroll_to_text(UIText.SIGN_OUT_BTN)
        self.tap_text(UIText.SIGN_OUT_BTN)

    def confirm_sign_out(self) -> None:
        """Confirm logout in the Alert dialog by tapping 'Sign Out'."""
        logger.info("Confirming Sign Out in dialog")
        # React Native Alert shows a dialog with "Cancel" and "Sign Out" buttons
        # On Android these are native Alert.alert() buttons
        try:
            # Try tapping the alert dialog "Sign Out" button
            self.wait_for_text_contains("Are you sure", timeout=8)
        except Exception:
            pass

        try:
            # Find the Sign Out button in the dialog
            # Android Alert renders with android.widget.Button elements
            from appium.webdriver.common.appiumby import AppiumBy
            btns = self.driver.find_elements(
                AppiumBy.CLASS_NAME, "android.widget.Button"
            )
            for btn in btns:
                if btn.text == "Sign Out" or btn.text == "SIGN OUT":
                    btn.click()
                    logger.info("Tapped Sign Out in alert dialog")
                    return
            # Fallback: tap by text
            self.tap_text("Sign Out")
        except Exception:
            # Last resort: tap the button by text directly
            try:
                self.tap_text("Sign Out")
            except Exception as exc:
                logger.error("Could not confirm sign out: %s", exc)

    def cancel_sign_out(self) -> None:
        """Cancel the logout dialog."""
        logger.info("Cancelling Sign Out dialog")
        try:
            btns = self.driver.find_elements(
                AppiumBy.CLASS_NAME, "android.widget.Button"
            )
            for btn in btns:
                if btn.text in ("Cancel", "CANCEL"):
                    btn.click()
                    return
            self.tap_text("Cancel")
        except Exception as exc:
            logger.warning("Cancel sign out failed: %s", exc)

    def logout(self) -> None:
        """Full logout: tap Sign Out → confirm in dialog."""
        self.tap_sign_out()
        time.sleep(1)
        self.confirm_sign_out()

    def update_profile(self, phone: str = "", clinic: str = "") -> None:
        """Update profile fields and save."""
        if phone:
            self.enter_phone(phone)
        if clinic:
            self.enter_clinic(clinic)
        self.tap_save_changes()

    def wait_for_login_screen_after_logout(self, timeout: int = 15) -> bool:
        """After logout, wait until the Login screen is visible."""
        try:
            self.wait_for_text(UIText.LOGIN_HEADING, timeout=timeout)
            return True
        except Exception:
            # Also accept the brand name being visible
            return self.is_text_visible(UIText.BRAND_NAME, timeout=5)
