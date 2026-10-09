"""
DentAI Appium — Signup Page Object
=====================================
Locators verified against:  DentAI-Mobile/src/screens/SignupScreen.tsx

UI elements:
  - "DentAI" brand + "CBCT AI Segmentation Platform"
  - "Create your account" heading
  - "Join the platform — clinical access only" subheading
  - Full Name EditText       [1]
  - License Number EditText  [2]
  - Email address EditText   [3]
  - Password EditText        [4]
  - Password strength bar + label
  - "Create Account" button
  - Success alert: "Account created! Redirecting to login…"
  - Error alert
  - "Already have an account? Sign in" link
"""

import logging
from appium_tests.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from appium_tests.pages.base_page import BasePage
from appium_tests.utils.test_data import UIText
from appium_tests.config.config import EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class SignupPage(BasePage):
    """Page object for the DentAI Mobile Signup screen."""

    # ── Verifications ──────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return (
            self.is_text_visible(UIText.BRAND_NAME)
            and self.is_text_visible(UIText.SIGNUP_HEADING)
            and self.is_text_visible(UIText.CREATE_ACCOUNT_BTN)
        )

    def get_error_message(self) -> str:
        for fragment in ("All fields", "Password must", "Signup failed", "Cannot"):
            try:
                el = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{fragment}")',
                )
                return el.text
            except Exception:
                continue
        return ""

    def get_success_message(self) -> str:
        try:
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Account created")',
            )
            return el.text
        except Exception:
            return ""

    def is_success_visible(self) -> bool:
        return self.is_text_contains_visible("Account created", timeout=5)

    def get_password_strength_label(self) -> str:
        """Return password strength label text (e.g. 'Strong', 'Weak')."""
        for label in ("Very Strong", "Strong", "Fair", "Weak", "Very Weak"):
            if self.is_text_visible(label, timeout=2):
                return label
        return ""

    # ── Actions ────────────────────────────────────────────────────────────────

    def enter_full_name(self, name: str) -> "SignupPage":
        logger.info("Entering full name: %s", name)
        self.type_into_field(1, name)
        return self

    def enter_license_number(self, license_no: str) -> "SignupPage":
        logger.info("Entering license: %s", license_no)
        self.type_into_field(2, license_no)
        return self

    def enter_email(self, email: str) -> "SignupPage":
        logger.info("Entering email: %s", email)
        self.type_into_field(3, email)
        return self

    def enter_password(self, password: str) -> "SignupPage":
        logger.info("Entering password")
        self.type_into_field(4, password)
        return self

    def tap_create_account(self) -> None:
        logger.info("Tapping Create Account")
        self.hide_keyboard()
        self.tap_text(UIText.CREATE_ACCOUNT_BTN)

    def tap_sign_in_link(self) -> None:
        """Tap 'Sign in' link to go back to Login."""
        self.tap_text("Sign in")

    def register(
        self, name: str, license_no: str, email: str, password: str
    ) -> None:
        """
        Complete registration flow.
        Caller should check is_success_visible() after calling this.
        """
        logger.info("Registering user: %s / %s", name, email)
        self.enter_full_name(name)
        self.enter_license_number(license_no)
        self.enter_email(email)
        self.enter_password(password)
        self.tap_create_account()

    def wait_for_success(self, timeout: int = 10) -> bool:
        try:
            self.wait_for_text_contains("Account created", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_signup_screen(self, timeout: int = 15) -> bool:
        try:
            self.wait_for_text(UIText.SIGNUP_HEADING, timeout=timeout)
            return True
        except Exception:
            return False
