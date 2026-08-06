"""
Signup Page Object Model
"""
from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage


class SignupPage(BasePage):
    NAME_INPUT      = (By.CSS_SELECTOR, "input[name='name'], #name, input[placeholder*='name' i]")
    LICENSE_INPUT   = (By.CSS_SELECTOR, "input[name='license'], #license, input[placeholder*='license' i]")
    EMAIL_INPUT     = (By.CSS_SELECTOR, "input[type='email'], input[name='email'], #email")
    PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[type='password'], input[name='password'], #password")
    SUBMIT_BTN      = (By.CSS_SELECTOR, "button[type='submit'], .signup-btn, #signup-btn, button")
    LOGIN_LINK      = (By.CSS_SELECTOR, "a[href*='login'], .login-link")
    ERROR_MSG       = (By.CSS_SELECTOR, ".error-message, .alert-danger, .error, [class*='error']")
    SUCCESS_MSG     = (By.CSS_SELECTOR, ".success-message, .alert-success, [class*='success']")
    FORM            = (By.CSS_SELECTOR, "form, .signup-form, .register-form")

    def open(self):
        return super().open("signup")

    def enter_name(self, name: str):
        self.type_text(*self.NAME_INPUT, name); return self

    def enter_license(self, license_num: str):
        self.type_text(*self.LICENSE_INPUT, license_num); return self

    def enter_email(self, email: str):
        self.type_text(*self.EMAIL_INPUT, email); return self

    def enter_password(self, password: str):
        self.type_text(*self.PASSWORD_INPUT, password); return self

    def click_submit(self):
        self.click(*self.SUBMIT_BTN); return self

    def signup(self, name, license_num, email, password):
        self.open()
        self.enter_name(name)
        self.enter_license(license_num)
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        return self

    def get_error_message(self) -> str:
        if self.is_visible(*self.ERROR_MSG, timeout=5):
            return self.get_text(*self.ERROR_MSG)
        return ""

    def is_on_signup_page(self) -> bool:
        return "signup" in self.get_current_url().lower()

    def all_fields_visible(self) -> bool:
        return all([
            self.is_visible(*self.NAME_INPUT),
            self.is_visible(*self.EMAIL_INPUT),
            self.is_visible(*self.PASSWORD_INPUT),
            self.is_visible(*self.SUBMIT_BTN),
        ])
