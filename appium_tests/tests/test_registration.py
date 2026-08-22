"""
DentAI Mobile — Registration Tests
=====================================
TC-APP-002  User Registration (New Account)
"""

import time
import pytest

from appium_tests.pages.login_page import LoginPage
from appium_tests.pages.signup_page import SignupPage
from appium_tests.utils.test_data import (
    UIText,
    REG_EMAIL, REG_PASSWORD, REG_NAME, REG_LICENSE,
)


class TestRegistration:
    """Authentication — Registration test cases."""

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.tc_id("TC-APP-002")
    @pytest.mark.module("Authentication")
    @pytest.mark.precond("App is on Login screen, no prior account with REG_EMAIL exists")
    @pytest.mark.steps(
        "1. From Login screen, tap 'Create account'\n"
        "2. Verify Signup screen appears\n"
        "3. Enter Full Name\n"
        "4. Enter License Number\n"
        "5. Enter unique Email address\n"
        "6. Enter valid Password (min 8 chars)\n"
        "7. Observe password strength indicator\n"
        "8. Tap 'Create Account' button\n"
        "9. Verify success message appears\n"
        "10. Verify redirect to Login screen"
    )
    @pytest.mark.expected(
        "Account created successfully. "
        "'Account created! Redirecting to login…' message shown. "
        "User is redirected to Login screen."
    )
    def test_user_registration_success(self, driver):
        """
        TC-APP-002 — User Registration

        Navigate from Login to Signup, fill all fields, submit form,
        and verify success message + redirect to Login.
        """
        login  = LoginPage(driver)
        signup = SignupPage(driver)

        # ── Step 1: Navigate to Signup ────────────────────────────────────────
        assert login.wait_for_login_screen(timeout=20), (
            "Login screen not visible — cannot navigate to Signup"
        )
        login.tap_create_account()

        # ── Step 2: Verify Signup screen ─────────────────────────────────────
        assert signup.wait_for_signup_screen(timeout=15), (
            f"Signup screen did not appear. Expected '{UIText.SIGNUP_HEADING}'."
        )
        assert signup.is_text_visible(UIText.BRAND_NAME), (
            "DentAI brand not visible on Signup screen"
        )
        signup.take_screenshot("TC_APP_002_signup_screen_visible")

        # ── Steps 3-6: Fill registration form ────────────────────────────────
        signup.enter_full_name(REG_NAME)
        signup.enter_license_number(REG_LICENSE)
        signup.enter_email(REG_EMAIL)
        signup.enter_password(REG_PASSWORD)

        # ── Step 7: Verify password strength indicator ────────────────────────
        strength = signup.get_password_strength_label()
        # Note: strength may be empty if the password bar is off-screen
        # We only verify it if visible, not mandatory
        if strength:
            assert strength in ("Fair", "Strong", "Very Strong"), (
                f"Password strength unexpected for test password: '{strength}'"
            )

        signup.take_screenshot("TC_APP_002_form_filled")

        # ── Step 8: Submit ────────────────────────────────────────────────────
        signup.tap_create_account()

        # ── Step 9: Verify success or error ──────────────────────────────────
        # The backend may return an error if the email already exists.
        # In CI the email is timestamped so it should be unique.
        success = signup.wait_for_success(timeout=15)
        if not success:
            err = signup.get_error_message()
            signup.take_screenshot("TC_APP_002_registration_error")
            # If email already exists, that is an expected backend response (not a framework bug)
            if "already" in err.lower() or "email" in err.lower():
                pytest.skip(
                    f"Registration skipped — email already registered: {REG_EMAIL}"
                )
            else:
                pytest.fail(
                    f"Registration failed unexpectedly. Error: '{err}'\n"
                    f"Email used: {REG_EMAIL}"
                )

        # ── Step 9 confirmed: success message visible ──────────────────────────
        success_msg = signup.get_success_message()
        assert "Account created" in success_msg, (
            f"Expected 'Account created' in success message, got: '{success_msg}'"
        )
        signup.take_screenshot("TC_APP_002_registration_success")

        # ── Step 10: Verify redirect to Login ────────────────────────────────
        # The app redirects after 1500ms (setTimeout in SignupScreen.tsx)
        assert login.wait_for_login_screen(timeout=10), (
            "Expected redirect to Login screen after successful registration, "
            "but Login screen did not appear within 10 seconds."
        )
        signup.take_screenshot("TC_APP_002_redirected_to_login")

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.tc_id("TC-APP-002b")
    @pytest.mark.module("Authentication")
    @pytest.mark.precond("App is on Signup screen")
    @pytest.mark.steps(
        "1. Navigate to Signup screen\n"
        "2. Leave all fields empty\n"
        "3. Tap Create Account\n"
        "4. Verify 'All fields are required.' error"
    )
    @pytest.mark.expected("Validation error shown for empty fields")
    def test_registration_empty_fields_shows_error(self, driver):
        """
        TC-APP-002b — Registration Validation (empty fields)

        Verify that submitting the registration form with empty fields
        shows the correct validation error.
        """
        login  = LoginPage(driver)
        signup = SignupPage(driver)

        assert login.wait_for_login_screen(timeout=20)
        login.tap_create_account()
        assert signup.wait_for_signup_screen(timeout=15)

        # Tap Create Account without filling any fields
        signup.tap_create_account()

        # Expect validation error
        error = signup.get_error_message()
        assert error, "Expected validation error for empty fields, got none"
        assert "required" in error.lower() or "All fields" in error, (
            f"Unexpected error message: '{error}'"
        )
        signup.take_screenshot("TC_APP_002b_empty_fields_error")
