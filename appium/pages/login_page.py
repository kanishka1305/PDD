"""
DentAI Appium — Login Page Object
====================================
Locators verified against:  DentAI-Mobile/src/screens/LoginScreen.tsx

UI elements present on screen:
  - Brand "DentAI" text
  - "CBCT AI Segmentation Platform" subtitle
  - "Welcome back" heading
  - "Sign in to your clinical account" subheading
  - Email address EditText  [1st EditText]
  - Password EditText       [2nd EditText]
  - Eye/toggle password     (emoji text "👁️")
  - "Forgot password?" link
  - "Sign In" button
  - "or" divider
  - "Create account" link
  - Error alert text (e.g. "Please enter your email and password.")
"""

import logging
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from appium.pages.base_page import BasePage
from appium.utils.test_data import UIText

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page object for the DentAI Mobile Login screen."""

    # ── Locators ───────────────────────────────────────────────────────────────
    # Verified against LoginScreen.tsx source code

    @property
    def _email_field(self):
        """First EditText on screen — email address input."""
        return self.wait.until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, "(//android.widget.EditText)[1]")
            )
        )

    @property
    def _password_field(self):
        """Second EditText on screen — password input."""
        return self.wait.until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, "(//android.widget.EditText)[2]")
            )
        )

    # ── Verifications ──────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        """Verify the Login screen is fully displayed."""
        return (
            self.is_text_visible(UIText.BRAND_NAME)
            and self.is_text_visible(UIText.LOGIN_HEADING)
            and self.is_text_visible(UIText.SIGN_IN_BTN)
        )

    def verify_brand(self) -> bool:
        """Assert DentAI brand elements are visible."""
        return (
            self.is_text_visible(UIText.BRAND_NAME)
            and self.is_text_visible(UIText.BRAND_SUBTITLE)
        )

    def get_error_message(self) -> str:
        """Return the error alert text if visible, else empty string."""
        # Error messages from source: "Please enter your email and password."
        #                             "Invalid email or password."
        #                             "Cannot reach server…"
        for fragment in ("Please", "Invalid", "Cannot", "required"):
            try:
                el = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{fragment}")',
                )
                return el.text
            except Exception:
                continue
        return ""

    def is_error_visible(self) -> bool:
        return bool(self.get_error_message())

    # ── Actions ────────────────────────────────────────────────────────────────

    def enter_email(self, email: str) -> "LoginPage":
        logger.info("Entering email: %s", email)
        el = self._email_field
        el.clear()
        el.send_keys(email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        logger.info("Entering password")
        el = self._password_field
        el.clear()
        el.send_keys(password)
        return self

    def tap_sign_in(self) -> None:
        """Tap the Sign In button."""
        logger.info("Tapping Sign In")
        self.hide_keyboard()
        self.tap_text(UIText.SIGN_IN_BTN)

    def tap_forgot_password(self) -> None:
        logger.info("Tapping Forgot password?")
        self.tap_text(UIText.FORGOT_PASSWORD_LINK)

    def tap_create_account(self) -> None:
        logger.info("Tapping Create account link")
        self.tap_text(UIText.CREATE_ACCOUNT_LINK)

    def toggle_password_visibility(self) -> None:
        """Tap the eye icon to show/hide password."""
        try:
            self.tap_text("👁️")
        except Exception:
            try:
                self.tap_text("🙈")
            except Exception:
                logger.warning("Password toggle button not found")

    def login(self, email: str, password: str) -> None:
        """
        Complete login flow: enter credentials and tap Sign In.
        Does NOT wait for dashboard — caller should verify next screen.
        """
        logger.info("Performing login for: %s", email)
        self.enter_email(email)
        self.enter_password(password)
        self.tap_sign_in()

    def wait_for_login_screen(self, timeout: int = 15) -> bool:
        """Wait until the login screen is visible."""
        try:
            self.wait_for_text(UIText.LOGIN_HEADING, timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_error(self, timeout: int = 10) -> str:
        """Wait for an error message to appear and return its text."""
        try:
            for fragment in ("Please", "Invalid", "Cannot"):
                try:
                    el = self.wait_for_text_contains(fragment, timeout=timeout)
                    return el.text
                except Exception:
                    continue
        except Exception:
            pass
        return ""
