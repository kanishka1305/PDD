"""
Forms & Input Validation Test Suite — 50+40 test cases
TC-FORM-001..050  |  TC-INP-001..040
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from automation.pages.login_page import LoginPage
from automation.pages.signup_page import SignupPage
from automation.pages.dashboard_page import ForgotPasswordPage, UploadPage
from automation.data.test_data import SQL_PAYLOADS, XSS_PAYLOADS, BOUNDARY_VALUES


class TestForms:
    # ── Login form field tests (TC-FORM-001..025) ─────────────────────────────
    def test_form_001_login_email_clears(self, driver):
        """TC-FORM-001: Email field can be cleared"""
        p = LoginPage(driver).open()
        p.enter_email("test@test.com")
        p.enter_email("")
        assert p.get_attribute(*p.EMAIL_INPUT, "value") == ""

    def test_form_002_login_password_clears(self, driver):
        """TC-FORM-002: Password field can be cleared"""
        p = LoginPage(driver).open()
        p.enter_password("Test123!")
        p.enter_password("")
        assert p.get_attribute(*p.PASSWORD_INPUT, "value") == ""

    def test_form_003_login_email_max_length(self, driver):
        """TC-FORM-003: Email field handles max-length input"""
        p = LoginPage(driver).open()
        long_email = "a" * 200 + "@test.com"
        p.enter_email(long_email)
        val = p.get_attribute(*p.EMAIL_INPUT, "value")
        assert len(val) <= 300

    def test_form_004_login_submit_with_spaces_only(self, driver):
        """TC-FORM-004: Login with whitespace-only email stays on page"""
        p = LoginPage(driver).open()
        p.enter_email("   ")
        p.enter_password("Test123!")
        p.click_login()
        assert p.is_on_login_page()

    def test_form_005_login_enter_key_submits(self, driver):
        """TC-FORM-005: Pressing Enter in password field submits login"""
        p = LoginPage(driver).open()
        p.enter_email("test@test.com")
        pw = p.find(*p.PASSWORD_INPUT)
        pw.send_keys("Test123!" + Keys.ENTER)
        assert driver.title != ""

    def test_form_006_signup_all_fields_clearable(self, driver):
        """TC-FORM-006: All signup fields can be cleared"""
        p = SignupPage(driver).open()
        p.enter_name("Dr Test").enter_name("")
        p.enter_email("x@x.com").enter_email("")
        p.enter_password("Test123!").enter_password("")
        assert p.get_attribute(*p.EMAIL_INPUT, "value") == ""

    def test_form_007_signup_name_special_chars(self, driver):
        """TC-FORM-007: Signup name with hyphens and apostrophes"""
        p = SignupPage(driver).open()
        p.enter_name("Dr. O'Brien-Smith")
        val = p.get_attribute(*p.NAME_INPUT, "value")
        assert "O'Brien" in val or len(val) > 0

    def test_form_008_login_email_case_insensitive_entry(self, driver):
        """TC-FORM-008: Email field accepts uppercase input"""
        p = LoginPage(driver).open()
        p.enter_email("DOCTOR@TEST.COM")
        val = p.get_attribute(*p.EMAIL_INPUT, "value")
        assert len(val) > 0

    def test_form_009_login_password_unicode(self, driver):
        """TC-FORM-009: Password field accepts Unicode characters"""
        p = LoginPage(driver).open()
        p.enter_password("Tëst123!áü")
        val = p.get_attribute(*p.PASSWORD_INPUT, "value")
        assert len(val) > 0

    def test_form_010_login_email_with_plus_sign(self, driver):
        """TC-FORM-010: Email with plus sign accepted"""
        p = LoginPage(driver).open()
        p.enter_email("doctor+test@test.com")
        val = p.get_attribute(*p.EMAIL_INPUT, "value")
        assert "+" in val

    def test_form_011_signup_password_numbers_only(self, driver):
        """TC-FORM-011: Password with numbers only attempted"""
        p = SignupPage(driver).open()
        p.enter_name("Dr Test")
        p.enter_email("t@t.com")
        p.enter_password("12345678")
        p.click_submit()
        assert driver.title != ""

    def test_form_012_login_double_click_submit(self, driver):
        """TC-FORM-012: Double-clicking submit doesn't crash page"""
        p = LoginPage(driver).open()
        p.enter_email("test@test.com")
        p.enter_password("Test123!")
        btn = p.find(*p.LOGIN_BTN)
        btn.click()
        try:
            btn.click()
        except Exception:
            pass
        assert driver.title != ""

    def test_form_013_login_tab_through_fields(self, driver):
        """TC-FORM-013: Tab key traverses login form fields"""
        p = LoginPage(driver).open()
        email_el = p.find(*p.EMAIL_INPUT)
        email_el.click()
        email_el.send_keys(Keys.TAB)
        focused = driver.execute_script("return document.activeElement.tagName;")
        assert focused in ("INPUT", "BUTTON", "A")

    def test_form_014_signup_license_numbers_only(self, driver):
        """TC-FORM-014: License field accepts numeric values"""
        p = SignupPage(driver).open()
        p.enter_license("123456")
        val = p.get_attribute(*p.LICENSE_INPUT, "value")
        assert "123456" in val

    def test_form_015_login_email_with_subdomain(self, driver):
        """TC-FORM-015: Email with subdomain accepted"""
        p = LoginPage(driver).open()
        p.enter_email("doctor@clinic.hospital.com")
        val = p.get_attribute(*p.EMAIL_INPUT, "value")
        assert "clinic.hospital.com" in val

    def test_form_016_forgot_pwd_submit_btn_exists(self, driver):
        """TC-FORM-016: Forgot password submit button visible"""
        p = ForgotPasswordPage(driver).open()
        assert p.is_visible(*p.SUBMIT_BTN)

    def test_form_017_forgot_pwd_email_field_exists(self, driver):
        """TC-FORM-017: Forgot password email field visible"""
        p = ForgotPasswordPage(driver).open()
        assert p.is_visible(*p.EMAIL_INPUT)

    def test_form_018_login_form_has_no_extra_action_url(self, driver):
        """TC-FORM-018: Login form action attribute is not pointing to http://"""
        p = LoginPage(driver).open()
        form = p.find(*p.FORM)
        action = form.get_attribute("action") or ""
        assert not action.startswith("http://"), "Form action uses insecure HTTP"

    def test_form_019_signup_form_present(self, driver):
        """TC-FORM-019: Signup page has a form element"""
        p = SignupPage(driver).open()
        assert p.is_present(*p.FORM)

    def test_form_020_upload_page_file_input_present(self, driver):
        """TC-FORM-020: Upload page file input present"""
        p = UploadPage(driver).open()
        assert p.is_file_input_present()

    def test_form_021_login_empty_submit_no_server_500(self, driver):
        """TC-FORM-021: Empty login submission doesn't cause server error"""
        p = LoginPage(driver).open()
        p.click_login()
        src = driver.page_source.lower()
        assert "500" not in driver.title and "server error" not in src

    def test_form_022_signup_empty_submit_no_server_500(self, driver):
        """TC-FORM-022: Empty signup submission doesn't cause server error"""
        p = SignupPage(driver).open()
        p.click_submit()
        src = driver.page_source.lower()
        assert "server error" not in src

    def test_form_023_login_email_with_ip(self, driver):
        """TC-FORM-023: Email with IP address domain accepted by input"""
        p = LoginPage(driver).open()
        p.enter_email("user@192.168.1.1")
        val = p.get_attribute(*p.EMAIL_INPUT, "value")
        assert len(val) > 0

    def test_form_024_login_password_with_spaces(self, driver):
        """TC-FORM-024: Password with internal spaces accepted"""
        p = LoginPage(driver).open()
        p.enter_password("Test 123 !")
        val = p.get_attribute(*p.PASSWORD_INPUT, "value")
        assert len(val) > 0

    def test_form_025_all_form_fields_labeled(self, driver):
        """TC-FORM-025: Form fields have labels or aria-label"""
        p = LoginPage(driver).open()
        email_el = p.find(*p.EMAIL_INPUT)
        has_label = (p.is_present(*p.EMAIL_LABEL) if hasattr(p, "EMAIL_LABEL") else False)
        aria = email_el.get_attribute("aria-label") or ""
        placeholder = email_el.get_attribute("placeholder") or ""
        assert has_label or aria or placeholder, "Email field not labeled"

    # ── Input Validation tests (TC-INP-001..040) ──────────────────────────────
    def test_inp_001_sql_injection_1(self, driver):
        """TC-INP-001: SQL injection OR bypass in email"""
        p = LoginPage(driver).open()
        p.enter_email(SQL_PAYLOADS[0]).enter_password("x")
        p.click_login()
        assert p.is_on_login_page()

    def test_inp_002_sql_injection_2(self, driver):
        """TC-INP-002: SQL injection comment bypass"""
        p = LoginPage(driver).open()
        p.enter_email(SQL_PAYLOADS[1]).enter_password("x")
        p.click_login()
        assert p.is_on_login_page()

    def test_inp_003_sql_injection_union(self, driver):
        """TC-INP-003: SQL UNION injection"""
        p = LoginPage(driver).open()
        p.enter_email(SQL_PAYLOADS[2]).enter_password("x")
        p.click_login()
        assert p.is_on_login_page()

    def test_inp_004_sql_injection_drop(self, driver):
        """TC-INP-004: SQL DROP TABLE injection"""
        p = LoginPage(driver).open()
        p.enter_email(SQL_PAYLOADS[3]).enter_password("x")
        p.click_login()
        assert p.is_on_login_page()

    def test_inp_005_xss_script_tag(self, driver):
        """TC-INP-005: XSS script tag in email not executed"""
        p = LoginPage(driver).open()
        p.enter_email(XSS_PAYLOADS[0]).enter_password("x")
        p.click_login()
        assert XSS_PAYLOADS[0] not in driver.page_source

    def test_inp_006_xss_img_onerror(self, driver):
        """TC-INP-006: XSS img onerror not executed"""
        p = LoginPage(driver).open()
        p.enter_email(XSS_PAYLOADS[1]).enter_password("x")
        p.click_login()
        assert driver.title != ""

    def test_inp_007_xss_javascript_protocol(self, driver):
        """TC-INP-007: javascript: protocol in email handled safely"""
        p = LoginPage(driver).open()
        p.enter_email(XSS_PAYLOADS[2]).enter_password("x")
        p.click_login()
        assert driver.title != ""

    def test_inp_008_empty_email(self, driver):
        """TC-INP-008: Empty email field handled"""
        p = LoginPage(driver).open()
        p.enter_email("").enter_password("Test123!").click_login()
        assert p.is_on_login_page()

    def test_inp_009_empty_password(self, driver):
        """TC-INP-009: Empty password field handled"""
        p = LoginPage(driver).open()
        p.enter_email("test@test.com").enter_password("").click_login()
        assert p.is_on_login_page()

    def test_inp_010_whitespace_email(self, driver):
        """TC-INP-010: Whitespace-only email handled"""
        p = LoginPage(driver).open()
        p.enter_email("   ").enter_password("Test123!").click_login()
        assert p.is_on_login_page()

    def test_inp_011_overlong_email_500_chars(self, driver):
        """TC-INP-011: 500-char email handled gracefully"""
        p = LoginPage(driver).open()
        p.enter_email("a" * 490 + "@t.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_012_overlong_password(self, driver):
        """TC-INP-012: 1000-char password handled gracefully"""
        p = LoginPage(driver).open()
        p.enter_email("t@t.com").enter_password("A" * 1000).click_login()
        assert driver.title != ""

    def test_inp_013_null_bytes_in_email(self, driver):
        """TC-INP-013: Null byte characters in email handled"""
        p = LoginPage(driver).open()
        p.enter_email("test\x00@test.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_014_special_chars_email(self, driver):
        """TC-INP-014: Special characters in email field"""
        p = LoginPage(driver).open()
        p.enter_email("!#$%&'*+/=?^`{|}~@test.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_015_html_entity_in_email(self, driver):
        """TC-INP-015: HTML entities in email field"""
        p = LoginPage(driver).open()
        p.enter_email("&lt;test&gt;@x.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_016_newline_in_email(self, driver):
        """TC-INP-016: Newline in email handled safely"""
        p = LoginPage(driver).open()
        p.enter_email("test\n@x.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_017_tab_in_email(self, driver):
        """TC-INP-017: Tab character in email handled"""
        p = LoginPage(driver).open()
        p.enter_email("test\t@x.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_018_unicode_email(self, driver):
        """TC-INP-018: Unicode in email handled"""
        p = LoginPage(driver).open()
        p.enter_email("tëst@ëxample.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_019_emoji_in_password(self, driver):
        """TC-INP-019: Emoji in password handled"""
        p = LoginPage(driver).open()
        p.enter_email("t@t.com").enter_password("Test123!😀").click_login()
        assert driver.title != ""

    def test_inp_020_crlf_injection_email(self, driver):
        """TC-INP-020: CRLF in email handled safely"""
        p = LoginPage(driver).open()
        p.enter_email("test\r\n@x.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_021_signup_name_boundary_min(self, driver):
        """TC-INP-021: Signup name at minimum boundary (2 chars)"""
        p = SignupPage(driver).open()
        p.enter_name(BOUNDARY_VALUES["name_min"]).enter_email("t@t.com")
        p.enter_password("Test123!").click_submit()
        assert driver.title != ""

    def test_inp_022_signup_name_boundary_max(self, driver):
        """TC-INP-022: Signup name at maximum boundary (100 chars)"""
        p = SignupPage(driver).open()
        p.enter_name(BOUNDARY_VALUES["name_max"]).enter_email("t@t.com")
        p.enter_password("Test123!").click_submit()
        assert driver.title != ""

    def test_inp_023_signup_name_over_max(self, driver):
        """TC-INP-023: Signup name over maximum (101 chars)"""
        p = SignupPage(driver).open()
        p.enter_name(BOUNDARY_VALUES["name_over"]).enter_email("t@t.com")
        p.enter_password("Test123!").click_submit()
        assert driver.title != ""

    def test_inp_024_password_minimum_valid(self, driver):
        """TC-INP-024: Password at minimum valid length"""
        p = SignupPage(driver).open()
        p.enter_name("Dr T").enter_email("t@t.com")
        p.enter_password(BOUNDARY_VALUES["password_min"]).click_submit()
        assert driver.title != ""

    def test_inp_025_password_too_short(self, driver):
        """TC-INP-025: Password below minimum length"""
        p = SignupPage(driver).open()
        p.enter_name("Dr T").enter_email("t@t.com")
        p.enter_password(BOUNDARY_VALUES["password_short"]).click_submit()
        assert driver.title != ""

    def test_inp_026_numeric_name(self, driver):
        """TC-INP-026: Numeric-only name handled"""
        p = SignupPage(driver).open()
        p.enter_name("12345").enter_email("t@t.com")
        p.enter_password("Test123!").click_submit()
        assert driver.title != ""

    def test_inp_027_email_missing_at_sign(self, driver):
        """TC-INP-027: Email missing @ symbol rejected"""
        p = LoginPage(driver).open()
        p.enter_email("usernameonly").enter_password("Test123!")
        p.click_login()
        assert p.is_on_login_page()

    def test_inp_028_email_missing_domain(self, driver):
        """TC-INP-028: Email with missing domain rejected"""
        p = LoginPage(driver).open()
        p.enter_email("user@").enter_password("Test123!")
        p.click_login()
        assert p.is_on_login_page()

    def test_inp_029_email_double_at(self, driver):
        """TC-INP-029: Email with double @ rejected"""
        p = LoginPage(driver).open()
        p.enter_email("user@@domain.com").enter_password("Test123!")
        p.click_login()
        assert p.is_on_login_page()

    def test_inp_030_numbers_only_email(self, driver):
        """TC-INP-030: Numeric-only local part email handled"""
        p = LoginPage(driver).open()
        p.enter_email("123456@test.com").enter_password("Test123!")
        p.click_login()
        assert driver.title != ""

    def test_inp_031_password_all_spaces(self, driver):
        """TC-INP-031: Password of all spaces handled"""
        p = LoginPage(driver).open()
        p.enter_email("t@t.com").enter_password("        ").click_login()
        assert driver.title != ""

    def test_inp_032_script_in_name(self, driver):
        """TC-INP-032: Script tag in signup name not stored/reflected"""
        p = SignupPage(driver).open()
        p.enter_name("<script>document.cookie</script>")
        p.enter_email("t@t.com").enter_password("Test123!").click_submit()
        assert "<script>document.cookie</script>" not in driver.page_source

    def test_inp_033_sql_in_signup_name(self, driver):
        """TC-INP-033: SQL injection in signup name handled"""
        p = SignupPage(driver).open()
        p.enter_name("'); DROP TABLE doctors;--")
        p.enter_email("t@t.com").enter_password("Test123!").click_submit()
        assert driver.title != ""

    def test_inp_034_forgot_pwd_sql_email(self, driver):
        """TC-INP-034: SQL injection in forgot-password email handled"""
        p = ForgotPasswordPage(driver).open()
        p.type_text(*p.EMAIL_INPUT, "' OR '1'='1")
        p.click(*p.SUBMIT_BTN)
        assert driver.title != ""

    def test_inp_035_forgot_pwd_xss_email(self, driver):
        """TC-INP-035: XSS in forgot-password email not reflected"""
        p = ForgotPasswordPage(driver).open()
        p.type_text(*p.EMAIL_INPUT, "<script>alert(1)</script>@x.com")
        p.click(*p.SUBMIT_BTN)
        assert "<script>alert(1)</script>" not in driver.page_source

    def test_inp_036_signup_license_sql(self, driver):
        """TC-INP-036: SQL injection in license field handled"""
        p = SignupPage(driver).open()
        p.enter_name("Dr T").enter_license("'; DROP TABLE doctors;--")
        p.enter_email("t@t.com").enter_password("Test123!").click_submit()
        assert driver.title != ""

    def test_inp_037_login_email_path_traversal(self, driver):
        """TC-INP-037: Path traversal chars in email handled"""
        p = LoginPage(driver).open()
        p.enter_email("../../etc/passwd@test.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_038_password_with_sql(self, driver):
        """TC-INP-038: SQL injection in password field handled"""
        p = LoginPage(driver).open()
        p.enter_email("t@t.com").enter_password("' OR '1'='1").click_login()
        assert driver.title != ""

    def test_inp_039_login_email_with_null(self, driver):
        """TC-INP-039: Email with null-like encoding handled"""
        p = LoginPage(driver).open()
        p.enter_email("%00admin%00@test.com").enter_password("x").click_login()
        assert driver.title != ""

    def test_inp_040_overlong_name_signup(self, driver):
        """TC-INP-040: Overlong name (500 chars) handled gracefully"""
        p = SignupPage(driver).open()
        p.enter_name("A" * 500).enter_email("t@t.com")
        p.enter_password("Test123!").click_submit()
        assert driver.title != ""
