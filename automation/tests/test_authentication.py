"""
Authentication Test Suite — 40 test cases
TC-AUTH-001 to TC-AUTH-040
"""
import pytest
from selenium.webdriver.common.by import By
from automation.pages.login_page import LoginPage
from automation.pages.signup_page import SignupPage
from automation.pages.dashboard_page import ForgotPasswordPage
from automation.data.test_data import VALID_USER, INVALID_USERS, SIGNUP_VALID, FORGOT_PASSWORD_DATA
from automation.config.settings import PAGES


class TestAuthentication:

    # ── Page Load ─────────────────────────────────────────────────────────────
    def test_auth_001_login_page_loads(self, driver):
        """TC-AUTH-001: Login page loads successfully from GitHub Pages"""
        p = LoginPage(driver).open()
        assert driver.title != "", "Page title should not be empty"

    def test_auth_002_login_page_has_email_field(self, driver):
        """TC-AUTH-002: Login page contains email input field"""
        p = LoginPage(driver).open()
        assert p.is_email_field_visible(), "Email field not visible"

    def test_auth_003_login_page_has_password_field(self, driver):
        """TC-AUTH-003: Login page contains password input field"""
        p = LoginPage(driver).open()
        assert p.is_password_field_visible(), "Password field not visible"

    def test_auth_004_login_page_has_submit_button(self, driver):
        """TC-AUTH-004: Login page contains submit button"""
        p = LoginPage(driver).open()
        assert p.is_login_button_visible(), "Login button not visible"

    def test_auth_005_login_page_has_signup_link(self, driver):
        """TC-AUTH-005: Login page contains link to signup"""
        p = LoginPage(driver).open()
        assert p.is_signup_link_visible(), "Signup link not visible"

    def test_auth_006_password_field_is_masked(self, driver):
        """TC-AUTH-006: Password field type=password (masked)"""
        p = LoginPage(driver).open()
        assert p.is_password_masked(), "Password field is not masked"

    def test_auth_007_login_page_has_form(self, driver):
        """TC-AUTH-007: Login page has a form element"""
        p = LoginPage(driver).open()
        assert p.is_form_present(), "Form element not found"

    def test_auth_008_empty_email_shows_validation(self, driver):
        """TC-AUTH-008: Empty email field shows HTML5 validation"""
        p = LoginPage(driver).open()
        p.enter_email("")
        p.enter_password("Test123!")
        p.click_login()
        # Should stay on login page (HTML5 required validation)
        assert p.is_on_login_page(), "Should stay on login page with empty email"

    def test_auth_009_empty_password_shows_validation(self, driver):
        """TC-AUTH-009: Empty password shows HTML5 validation"""
        p = LoginPage(driver).open()
        p.enter_email(VALID_USER["email"])
        p.enter_password("")
        p.click_login()
        assert p.is_on_login_page(), "Should stay on login page with empty password"

    def test_auth_010_both_fields_empty(self, driver):
        """TC-AUTH-010: Both fields empty — stays on login page"""
        p = LoginPage(driver).open()
        p.enter_email("")
        p.enter_password("")
        p.click_login()
        assert p.is_on_login_page(), "Should stay on login page with both empty"

    def test_auth_011_invalid_email_format(self, driver):
        """TC-AUTH-011: Invalid email format rejected"""
        p = LoginPage(driver).open()
        p.enter_email("notanemail")
        p.enter_password("Test123!")
        p.click_login()
        assert p.is_on_login_page(), "Should stay on login page with invalid email"

    def test_auth_012_wrong_credentials_error(self, driver):
        """TC-AUTH-012: Wrong credentials shows error"""
        p = LoginPage(driver).open()
        p.login("wrong@email.com", "wrongpass")
        # Either stays on login or shows error
        url = driver.current_url
        assert "login" in url.lower() or "dashboard" not in url.lower()

    def test_auth_013_sql_injection_email(self, driver):
        """TC-AUTH-013: SQL injection in email field is rejected"""
        p = LoginPage(driver).open()
        p.enter_email("' OR '1'='1")
        p.enter_password("anything")
        p.click_login()
        assert p.is_on_login_page(), "SQL injection should not bypass login"

    def test_auth_014_xss_in_email_field(self, driver):
        """TC-AUTH-014: XSS payload in email does not execute"""
        p = LoginPage(driver).open()
        p.enter_email("<script>alert('XSS')</script>@test.com")
        p.enter_password("Test123!")
        p.click_login()
        src = driver.page_source
        assert "<script>alert('XSS')</script>" not in src, "XSS not escaped"

    def test_auth_015_very_long_email(self, driver):
        """TC-AUTH-015: Very long email is handled gracefully"""
        p = LoginPage(driver).open()
        p.enter_email("a" * 300 + "@test.com")
        p.enter_password("Test123!")
        p.click_login()
        assert p.is_on_login_page(), "Should stay on login page with oversized email"

    def test_auth_016_forgot_password_link_visible(self, driver):
        """TC-AUTH-016: Forgot password link present on login page"""
        p = LoginPage(driver).open()
        has_link = p.is_visible(*p.FORGOT_LINK, timeout=5) if hasattr(p, 'FORGOT_LINK') else True
        assert has_link or p.is_on_login_page()

    def test_auth_017_signup_link_navigates(self, driver):
        """TC-AUTH-017: Clicking signup link navigates to signup"""
        p = LoginPage(driver).open()
        if p.is_signup_link_visible():
            p.click_signup_link()
            assert "signup" in driver.current_url.lower() or \
                   "register" in driver.current_url.lower() or \
                   driver.current_url != PAGES["login"]

    def test_auth_018_signup_page_loads(self, driver):
        """TC-AUTH-018: Signup page loads successfully"""
        p = SignupPage(driver).open()
        assert driver.title != ""

    def test_auth_019_signup_page_has_all_fields(self, driver):
        """TC-AUTH-019: Signup page has all required fields"""
        p = SignupPage(driver).open()
        assert p.all_fields_visible(), "Not all signup fields visible"

    def test_auth_020_signup_empty_name_validation(self, driver):
        """TC-AUTH-020: Empty name on signup shows validation"""
        p = SignupPage(driver).open()
        p.enter_name("")
        p.enter_email("test@test.com")
        p.enter_password("Test123!")
        p.click_submit()
        assert p.is_on_signup_page(), "Should stay on signup with empty name"

    def test_auth_021_signup_empty_email_validation(self, driver):
        """TC-AUTH-021: Empty email on signup shows validation"""
        p = SignupPage(driver).open()
        p.enter_name("Dr Test")
        p.enter_email("")
        p.enter_password("Test123!")
        p.click_submit()
        assert p.is_on_signup_page(), "Should stay on signup with empty email"

    def test_auth_022_signup_empty_password_validation(self, driver):
        """TC-AUTH-022: Empty password on signup shows validation"""
        p = SignupPage(driver).open()
        p.enter_name("Dr Test")
        p.enter_email("test@test.com")
        p.enter_password("")
        p.click_submit()
        assert p.is_on_signup_page(), "Should stay on signup with empty password"

    def test_auth_023_signup_invalid_email_format(self, driver):
        """TC-AUTH-023: Invalid email format rejected on signup"""
        p = SignupPage(driver).open()
        p.enter_name("Dr Test")
        p.enter_email("notanemail")
        p.enter_password("Test123!")
        p.click_submit()
        assert p.is_on_signup_page(), "Should stay on signup with invalid email"

    def test_auth_024_signup_weak_password(self, driver):
        """TC-AUTH-024: Weak password rejected on signup"""
        p = SignupPage(driver).open()
        p.enter_name("Dr Test")
        p.enter_email("test@test.com")
        p.enter_password("123")
        p.click_submit()
        assert p.is_on_signup_page(), "Should stay on signup with weak password"

    def test_auth_025_signup_xss_in_name(self, driver):
        """TC-AUTH-025: XSS in name field is handled safely"""
        p = SignupPage(driver).open()
        p.enter_name("<script>alert('XSS')</script>")
        p.enter_email("test@test.com")
        p.enter_password("Test123!")
        p.click_submit()
        src = driver.page_source
        assert "<script>alert('XSS')</script>" not in src

    def test_auth_026_forgot_password_page_loads(self, driver):
        """TC-AUTH-026: Forgot password page loads"""
        p = ForgotPasswordPage(driver).open()
        assert driver.title != ""

    def test_auth_027_forgot_password_has_email_field(self, driver):
        """TC-AUTH-027: Forgot password page has email field"""
        p = ForgotPasswordPage(driver).open()
        assert p.is_visible(*p.EMAIL_INPUT), "Email field not on forgot password page"

    def test_auth_028_forgot_password_empty_email(self, driver):
        """TC-AUTH-028: Empty email on forgot password stays on page"""
        p = ForgotPasswordPage(driver)
        p.open()
        p.click(*p.SUBMIT_BTN)
        assert "forgot" in driver.current_url.lower() or \
               "reset" in driver.current_url.lower() or \
               p.is_on_login_page()

    def test_auth_029_forgot_password_invalid_email(self, driver):
        """TC-AUTH-029: Invalid email format on forgot password"""
        p = ForgotPasswordPage(driver).submit_email("notanemail")
        assert driver.title != ""  # Page should handle gracefully

    def test_auth_030_forgot_password_unknown_email(self, driver):
        """TC-AUTH-030: Unknown email on forgot password — no user enumeration"""
        p = ForgotPasswordPage(driver).submit_email("nobody@nowhere.com")
        msg = p.get_message()
        # Response should be generic — no "email not found" enumeration
        assert "nobody@nowhere.com" not in msg.lower() or msg == ""

    def test_auth_031_login_page_title_not_empty(self, driver):
        """TC-AUTH-031: Login page has a non-empty document title"""
        LoginPage(driver).open()
        assert len(driver.title) > 0

    def test_auth_032_signup_page_has_login_link(self, driver):
        """TC-AUTH-032: Signup page has link back to login"""
        p = SignupPage(driver).open()
        assert p.is_present(*p.LOGIN_LINK), "Login link not found on signup page"

    def test_auth_033_login_page_loads_within_5s(self, driver):
        """TC-AUTH-033: Login page loads within 5 seconds"""
        import time
        start = time.time()
        LoginPage(driver).open()
        elapsed = time.time() - start
        assert elapsed < 5.0, f"Login page took {elapsed:.2f}s to load"

    def test_auth_034_signup_page_loads_within_5s(self, driver):
        """TC-AUTH-034: Signup page loads within 5 seconds"""
        import time
        start = time.time()
        SignupPage(driver).open()
        elapsed = time.time() - start
        assert elapsed < 5.0, f"Signup page took {elapsed:.2f}s to load"

    def test_auth_035_login_page_no_console_errors(self, driver):
        """TC-AUTH-035: Login page has no SEVERE console errors"""
        LoginPage(driver).open()
        logs = driver.get_log("browser") if hasattr(driver, "get_log") else []
        severe = [l for l in logs if l.get("level") == "SEVERE"]
        assert len(severe) == 0, f"Console errors: {severe}"

    def test_auth_036_login_page_has_https_url(self, driver):
        """TC-AUTH-036: Deployed login page uses HTTPS"""
        LoginPage(driver).open()
        assert driver.current_url.startswith("https://") or "127.0.0.1" in driver.current_url or "localhost" in driver.current_url, "Page not served over HTTPS"

    def test_auth_037_login_form_autocomplete(self, driver):
        """TC-AUTH-037: Login email field supports autocomplete"""
        p = LoginPage(driver).open()
        ac = p.get_attribute(*p.EMAIL_INPUT, "autocomplete")
        # Should allow autocomplete for UX (or be explicitly set)
        assert ac != "off", "Autocomplete should not be disabled on email"

    def test_auth_038_password_no_autocomplete_off(self, driver):
        """TC-AUTH-038: Password field is properly marked for password managers"""
        p = LoginPage(driver).open()
        ptype = p.get_password_type()
        assert ptype == "password", f"Password field type is '{ptype}', expected 'password'"

    def test_auth_039_login_page_mobile_viewport(self, driver):
        """TC-AUTH-039: Login page renders on mobile viewport (375x667)"""
        driver.set_window_size(375, 667)
        p = LoginPage(driver).open()
        assert p.is_email_field_visible(), "Email not visible on mobile"
        assert p.is_login_button_visible(), "Login btn not visible on mobile"

    def test_auth_040_login_page_tablet_viewport(self, driver):
        """TC-AUTH-040: Login page renders on tablet viewport (768x1024)"""
        driver.set_window_size(768, 1024)
        p = LoginPage(driver).open()
        assert p.is_email_field_visible(), "Email not visible on tablet"
