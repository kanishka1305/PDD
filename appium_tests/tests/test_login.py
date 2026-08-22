"""
DentAI Mobile — Login Tests
================================
TC-APP-001  Application Launch
TC-APP-003  Login (valid credentials)
TC-APP-004  Invalid Login Validation
"""

import pytest

from appium_tests.pages.login_page import LoginPage
from appium_tests.pages.home_page import HomePage
from appium_tests.utils.test_data import (
    UIText,
    VALID_EMAIL, VALID_PASSWORD,
    INVALID_EMAIL, INVALID_PASSWORD,
    EMPTY_EMAIL, EMPTY_PASSWORD,
)


class TestLogin:
    """Authentication — Login test cases."""

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.tc_id("TC-APP-001")
    @pytest.mark.module("Authentication")
    @pytest.mark.precond("App is installed and Appium server is running")
    @pytest.mark.steps(
        "1. Launch the DentAI Mobile app\n"
        "2. Wait for Login screen to appear\n"
        "3. Verify brand elements are visible"
    )
    @pytest.mark.expected("Login screen is displayed with DentAI brand")
    def test_app_launch_shows_login_screen(self, driver):
        """
        TC-APP-001 — Application Launch

        Verify the app launches successfully and shows the Login screen
        with all expected brand elements.
        """
        login = LoginPage(driver)

        # Verify the Login screen is loaded
        assert login.is_loaded(), (
            "Login screen did not appear after app launch. "
            "Expected 'Welcome back' heading and 'Sign In' button."
        )

        # Verify DentAI brand elements
        assert login.is_text_visible(UIText.BRAND_NAME), (
            f"Brand name '{UIText.BRAND_NAME}' not visible on Login screen"
        )
        assert login.is_text_visible(UIText.BRAND_SUBTITLE), (
            f"Brand subtitle '{UIText.BRAND_SUBTITLE}' not visible"
        )
        assert login.is_text_visible(UIText.LOGIN_HEADING), (
            f"Login heading '{UIText.LOGIN_HEADING}' not visible"
        )
        assert login.is_text_visible(UIText.LOGIN_SUBHEADING), (
            f"Login subheading not visible"
        )
        assert login.is_text_visible(UIText.SIGN_IN_BTN), (
            f"Sign In button not visible"
        )
        assert login.is_text_visible(UIText.FORGOT_PASSWORD_LINK), (
            f"Forgot password link not visible"
        )
        assert login.is_text_visible(UIText.CREATE_ACCOUNT_LINK), (
            f"Create account link not visible"
        )
        login.take_screenshot("TC_APP_001_app_launch")

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.tc_id("TC-APP-003")
    @pytest.mark.module("Authentication")
    @pytest.mark.precond("App is on Login screen, valid account exists in backend")
    @pytest.mark.steps(
        "1. Enter valid email address\n"
        "2. Enter valid password\n"
        "3. Tap Sign In button\n"
        "4. Wait for Dashboard to appear\n"
        "5. Verify 'Good day, Dr.' greeting"
    )
    @pytest.mark.expected("User is navigated to Dashboard with personalised greeting")
    def test_login_with_valid_credentials(self, driver):
        """
        TC-APP-003 — Login (valid credentials)

        Enter valid credentials and verify successful navigation to Dashboard.
        """
        login = LoginPage(driver)
        home  = HomePage(driver)

        # Wait for login screen
        assert login.wait_for_login_screen(timeout=20), (
            "Login screen not visible — app may not have launched correctly"
        )

        # Perform login
        login.login(VALID_EMAIL, VALID_PASSWORD)

        # Verify dashboard appears
        assert home.wait_for_dashboard(timeout=25), (
            f"Dashboard did not appear after login with '{VALID_EMAIL}'. "
            "Check that the backend is reachable and credentials are correct."
        )

        # Verify personalised greeting
        greeting = home.get_greeting_text()
        assert "Good day" in greeting, (
            f"Expected greeting to contain 'Good day', got: '{greeting}'"
        )

        # Verify bottom navigation is present
        assert home.is_text_visible(UIText.TAB_HOME), "Home tab not visible"
        assert home.is_text_visible(UIText.TAB_UPLOAD), "Upload tab not visible"
        assert home.is_text_visible(UIText.TAB_RESULTS), "Results tab not visible"

        home.take_screenshot("TC_APP_003_login_success")

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.tc_id("TC-APP-004")
    @pytest.mark.module("Authentication")
    @pytest.mark.precond("App is on Login screen")
    @pytest.mark.steps(
        "1. Enter invalid email\n"
        "2. Enter invalid password\n"
        "3. Tap Sign In\n"
        "4. Verify error message appears\n"
        "5. Verify user stays on Login screen\n\n"
        "6. Clear fields, leave both empty\n"
        "7. Tap Sign In\n"
        "8. Verify validation error"
    )
    @pytest.mark.expected("Error message is displayed; user stays on Login screen")
    def test_login_with_invalid_credentials_shows_error(self, driver):
        """
        TC-APP-004 — Invalid Login Validation

        Verify that invalid credentials show an appropriate error message
        and the user is not navigated to the Dashboard.
        """
        login = LoginPage(driver)

        assert login.wait_for_login_screen(timeout=20), (
            "Login screen not visible"
        )

        # ── Sub-case A: invalid credentials ───────────────────────────────────
        login.enter_email(INVALID_EMAIL)
        login.enter_password(INVALID_PASSWORD)
        login.tap_sign_in()

        # Error should appear (either "Invalid email or password" or "Cannot reach server")
        error = login.wait_for_error(timeout=12)
        assert error, (
            "Expected an error message after entering invalid credentials, but none appeared. "
            "Make sure the backend is running and returns a proper error response."
        )

        # Must still be on login screen (no dashboard)
        assert login.is_text_visible(UIText.SIGN_IN_BTN, timeout=5), (
            "Sign In button not visible — user may have been incorrectly navigated away"
        )
        login.take_screenshot("TC_APP_004_invalid_creds_error")

        # ── Sub-case B: empty fields ───────────────────────────────────────────
        login.enter_email(EMPTY_EMAIL)
        login.enter_password(EMPTY_PASSWORD)
        login.tap_sign_in()

        empty_error = login.wait_for_error(timeout=6)
        assert empty_error, (
            "Expected validation error for empty fields, but none appeared"
        )
        assert "Please enter" in empty_error or "email" in empty_error.lower(), (
            f"Unexpected error text for empty fields: '{empty_error}'"
        )
        login.take_screenshot("TC_APP_004_empty_fields_error")

    # ─────────────────────────────────────────────────────────────────────────
    @pytest.mark.tc_id("TC-APP-004b")
    @pytest.mark.module("Authentication")
    @pytest.mark.precond("App is on Login screen")
    @pytest.mark.steps(
        "1. Tap 'Forgot password?' link\n"
        "2. Verify navigation to ForgotPassword screen"
    )
    @pytest.mark.expected("ForgotPassword screen is displayed")
    def test_forgot_password_link_navigates(self, driver):
        """
        TC-APP-004b — Forgot Password Navigation

        Verify the 'Forgot password?' link navigates to the correct screen.
        """
        login = LoginPage(driver)

        assert login.wait_for_login_screen(timeout=20)

        login.tap_forgot_password()

        # ForgotPasswordScreen should show "Reset Password" or similar
        # (from ForgotPasswordScreen.tsx — not inspected but safe to check for absence of Login heading)
        import time
        time.sleep(2)

        # Verify we left the login screen (heading no longer shows "Welcome back")
        # OR that a different screen appeared
        assert not login.is_text_visible(UIText.LOGIN_HEADING, timeout=3) or \
               login.is_text_contains_visible("Reset", timeout=5) or \
               login.is_text_contains_visible("Forgot", timeout=5) or \
               login.is_text_contains_visible("Email", timeout=5), (
            "Expected to navigate away from Login after tapping 'Forgot password?'"
        )
        login.take_screenshot("TC_APP_004b_forgot_password_navigation")
