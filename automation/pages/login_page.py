"""
Login Page Object Model
"""
from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage


class LoginPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    EMAIL_INPUT     = (By.CSS_SELECTOR, "input[type='email'], input[name='email'], #email")
    PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[type='password'], input[name='password'], #password")
    LOGIN_BTN       = (By.CSS_SELECTOR, "button[type='submit'], .login-btn, #login-btn, button")
    SIGNUP_LINK     = (By.CSS_SELECTOR, "a[href*='signup'], .signup-link, a[href*='register']")
    FORGOT_LINK     = (By.CSS_SELECTOR, "a[href*='forgot'], .forgot-link")
    ERROR_MSG       = (By.CSS_SELECTOR, ".error-message, .alert-danger, .error, [class*='error']")
    SUCCESS_MSG     = (By.CSS_SELECTOR, ".success-message, .alert-success, [class*='success']")
    PAGE_HEADING    = (By.CSS_SELECTOR, "h1, h2, .page-title, .brand")
    LOGO            = (By.CSS_SELECTOR, ".logo, .brand-logo, img[alt*='logo'], img[alt*='Logo']")
    EMAIL_LABEL     = (By.CSS_SELECTOR, "label[for='email'], label[for*='email']")
    PASSWORD_LABEL  = (By.CSS_SELECTOR, "label[for='password'], label[for*='password']")
    FORM            = (By.CSS_SELECTOR, "form, .login-form")
    REMEMBER_ME     = (By.CSS_SELECTOR, "input[type='checkbox']")

    def open(self):
        return super().open("login")

    # ── Actions ───────────────────────────────────────────────────────────────
    def enter_email(self, email: str):
        self.type_text(*self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str):
        self.type_text(*self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(*self.LOGIN_BTN)
        return self

    def login(self, email: str, password: str):
        self.open()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self

    def click_signup_link(self):
        self.click(*self.SIGNUP_LINK)
        return self

    def click_forgot_password(self):
        self.click(*self.FORGOT_LINK)
        return self

    # ── Verifications ─────────────────────────────────────────────────────────
    def is_on_login_page(self) -> bool:
        return "login" in self.get_current_url().lower()

    def get_error_message(self) -> str:
        if self.is_visible(*self.ERROR_MSG, timeout=5):
            return self.get_text(*self.ERROR_MSG)
        return ""

    def is_email_field_visible(self) -> bool:
        return self.is_visible(*self.EMAIL_INPUT)

    def is_password_field_visible(self) -> bool:
        return self.is_visible(*self.PASSWORD_INPUT)

    def is_login_button_visible(self) -> bool:
        return self.is_visible(*self.LOGIN_BTN)

    def is_signup_link_visible(self) -> bool:
        return self.is_visible(*self.SIGNUP_LINK)

    def get_email_placeholder(self) -> str:
        return self.get_attribute(*self.EMAIL_INPUT, "placeholder")

    def get_password_type(self) -> str:
        return self.get_attribute(*self.PASSWORD_INPUT, "type")

    def is_password_masked(self) -> bool:
        return self.get_password_type() == "password"

    def is_form_present(self) -> bool:
        return self.is_present(*self.FORM)
