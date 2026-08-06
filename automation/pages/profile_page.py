"""
ProfilePage, WorkflowPage, RefinePage, ResetPasswordPage — Page Object Models

All locators use multi-strategy CSS selectors (id > name > class > attribute)
so they work regardless of minor HTML changes.
"""
from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage


# ─────────────────────────────────────────────────────────────────────────────
# PROFILE PAGE
# ─────────────────────────────────────────────────────────────────────────────

class ProfilePage(BasePage):
    """Covers: /profile or the profile section inside the dashboard."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Profile info fields
    NAME_INPUT         = (By.CSS_SELECTOR,
                          "#name, input[name='name'], input[placeholder*='name' i]")
    EMAIL_INPUT        = (By.CSS_SELECTOR,
                          "#email, input[type='email'], input[name='email']")
    PHONE_INPUT        = (By.CSS_SELECTOR,
                          "#phone, input[name='phone'], input[placeholder*='phone' i]")
    CLINIC_INPUT       = (By.CSS_SELECTOR,
                          "#clinic, input[name='clinic'], input[placeholder*='clinic' i]")
    LICENSE_INPUT      = (By.CSS_SELECTOR,
                          "#license, input[name='license'], input[placeholder*='license' i]")

    # Buttons
    SAVE_BTN           = (By.CSS_SELECTOR,
                          "#save-btn, button[id*='save'], button[class*='save'], "
                          "input[value*='Save' i], button[type='submit']")
    EDIT_BTN           = (By.CSS_SELECTOR,
                          "#edit-btn, button[id*='edit'], button[class*='edit'], "
                          ".edit-profile, a[href*='edit']")
    CANCEL_BTN         = (By.CSS_SELECTOR,
                          "#cancel-btn, button[class*='cancel'], .cancel-btn")

    # Change-password section
    CURRENT_PWD_INPUT  = (By.CSS_SELECTOR,
                          "#current-password, input[name='current_password'], "
                          "input[placeholder*='current' i][type='password']")
    NEW_PWD_INPUT      = (By.CSS_SELECTOR,
                          "#new-password, input[name='new_password'], "
                          "input[placeholder*='new password' i][type='password']")
    CONFIRM_PWD_INPUT  = (By.CSS_SELECTOR,
                          "#confirm-password, input[name='confirm_password'], "
                          "input[placeholder*='confirm' i][type='password']")
    CHANGE_PWD_BTN     = (By.CSS_SELECTOR,
                          "#change-password-btn, button[id*='change'], "
                          "button[class*='change-pwd'], button[class*='change-password']")

    # Credential section
    CRED_TYPE_INPUT    = (By.CSS_SELECTOR,
                          "#credential-type, input[name='credential_type'], "
                          "input[placeholder*='type' i]")
    CRED_NUMBER_INPUT  = (By.CSS_SELECTOR,
                          "#credential-number, input[name='credential_number'], "
                          "input[placeholder*='number' i]")
    CRED_ISSUE_INPUT   = (By.CSS_SELECTOR,
                          "#issue-date, input[name='issue_date'], "
                          "input[placeholder*='issue' i], input[type='date']:first-of-type")
    CRED_EXPIRY_INPUT  = (By.CSS_SELECTOR,
                          "#expiry-date, input[name='expiry_date'], "
                          "input[placeholder*='expiry' i], input[type='date']:last-of-type")
    ADD_CRED_BTN       = (By.CSS_SELECTOR,
                          "#add-credential-btn, button[id*='credential'], "
                          "button[class*='credential'], .add-credential")
    CRED_LIST          = (By.CSS_SELECTOR,
                          ".credential-list, .credentials, #credentials-table, "
                          "table[class*='credential'], .cred-row")

    # Feedback
    SUCCESS_MSG        = (By.CSS_SELECTOR,
                          ".success, .alert-success, [class*='success'], .toast-success")
    ERROR_MSG          = (By.CSS_SELECTOR,
                          ".error, .alert-danger, [class*='error'], .toast-error")
    AVATAR             = (By.CSS_SELECTOR,
                          ".avatar, .profile-pic, img[class*='avatar'], #profile-avatar")
    PROFILE_SECTION    = (By.CSS_SELECTOR,
                          ".profile-section, #profile, .profile-container, main")

    # ── Navigation ────────────────────────────────────────────────────────────
    def open(self):
        """Open the profile page — tries /profile.html then falls back to /dashboard.html."""
        try:
            return super().open("profile")
        except Exception:
            return super().open("dashboard")

    def is_on_profile_page(self) -> bool:
        url = self.get_current_url().lower()
        return "profile" in url or "dashboard" in url

    # ── Profile update actions ────────────────────────────────────────────────
    def enter_name(self, name: str):
        self.type_text(*self.NAME_INPUT, name)
        return self

    def enter_email(self, email: str):
        self.type_text(*self.EMAIL_INPUT, email)
        return self

    def enter_phone(self, phone: str):
        self.type_text(*self.PHONE_INPUT, phone)
        return self

    def enter_clinic(self, clinic: str):
        self.type_text(*self.CLINIC_INPUT, clinic)
        return self

    def click_save(self):
        self.click(*self.SAVE_BTN)
        return self

    def click_edit(self):
        if self.is_present(*self.EDIT_BTN):
            self.click(*self.EDIT_BTN)
        return self

    def update_profile(self, name: str = "", phone: str = "", clinic: str = ""):
        if name:
            self.enter_name(name)
        if phone:
            self.enter_phone(phone)
        if clinic:
            self.enter_clinic(clinic)
        self.click_save()
        return self

    # ── Change-password actions ───────────────────────────────────────────────
    def enter_current_password(self, pwd: str):
        self.type_text(*self.CURRENT_PWD_INPUT, pwd)
        return self

    def enter_new_password(self, pwd: str):
        self.type_text(*self.NEW_PWD_INPUT, pwd)
        return self

    def enter_confirm_password(self, pwd: str):
        self.type_text(*self.CONFIRM_PWD_INPUT, pwd)
        return self

    def click_change_password(self):
        self.click(*self.CHANGE_PWD_BTN)
        return self

    def change_password(self, current: str, new: str, confirm: str = ""):
        self.enter_current_password(current)
        self.enter_new_password(new)
        self.enter_confirm_password(confirm or new)
        self.click_change_password()
        return self

    # ── Credential actions ────────────────────────────────────────────────────
    def add_credential(self, cred_type: str, number: str,
                       issue: str = "2020-01-01", expiry: str = "2030-01-01"):
        if self.is_present(*self.CRED_TYPE_INPUT):
            self.type_text(*self.CRED_TYPE_INPUT, cred_type)
        if self.is_present(*self.CRED_NUMBER_INPUT):
            self.type_text(*self.CRED_NUMBER_INPUT, number)
        if self.is_present(*self.CRED_ISSUE_INPUT):
            self.type_text(*self.CRED_ISSUE_INPUT, issue)
        if self.is_present(*self.CRED_EXPIRY_INPUT):
            self.type_text(*self.CRED_EXPIRY_INPUT, expiry)
        if self.is_present(*self.ADD_CRED_BTN):
            self.click(*self.ADD_CRED_BTN)
        return self

    def get_credential_count(self) -> int:
        return self.element_count(*self.CRED_LIST)

    # ── Feedback helpers ──────────────────────────────────────────────────────
    def get_success_message(self) -> str:
        if self.is_visible(*self.SUCCESS_MSG, timeout=5):
            return self.get_text(*self.SUCCESS_MSG)
        return ""

    def get_error_message(self) -> str:
        if self.is_visible(*self.ERROR_MSG, timeout=5):
            return self.get_text(*self.ERROR_MSG)
        return ""

    def is_success_shown(self) -> bool:
        return self.is_visible(*self.SUCCESS_MSG, timeout=5)

    def is_error_shown(self) -> bool:
        return self.is_visible(*self.ERROR_MSG, timeout=5)

    # ── Field visibility helpers ──────────────────────────────────────────────
    def is_name_field_visible(self) -> bool:
        return self.is_visible(*self.NAME_INPUT)

    def is_email_field_visible(self) -> bool:
        return self.is_visible(*self.EMAIL_INPUT)

    def is_change_password_section_visible(self) -> bool:
        return (self.is_present(*self.CURRENT_PWD_INPUT)
                or self.is_present(*self.NEW_PWD_INPUT))

    def is_credentials_section_visible(self) -> bool:
        return (self.is_present(*self.CRED_TYPE_INPUT)
                or self.is_present(*self.CRED_LIST))


# ─────────────────────────────────────────────────────────────────────────────
# RESET PASSWORD PAGE
# ─────────────────────────────────────────────────────────────────────────────

class ResetPasswordPage(BasePage):
    """Covers: /reset-password.html?token=<token>"""

    # ── Locators ──────────────────────────────────────────────────────────────
    NEW_PWD_INPUT      = (By.CSS_SELECTOR,
                          "#new-password, input[name='new_password'], "
                          "input[placeholder*='new' i][type='password'], "
                          "input[type='password']:first-of-type")
    CONFIRM_PWD_INPUT  = (By.CSS_SELECTOR,
                          "#confirm-password, input[name='confirm_password'], "
                          "input[placeholder*='confirm' i][type='password'], "
                          "input[type='password']:last-of-type")
    TOKEN_INPUT        = (By.CSS_SELECTOR,
                          "#token, input[name='token'], input[type='hidden'][name*='token']")
    SUBMIT_BTN         = (By.CSS_SELECTOR,
                          "button[type='submit'], .reset-btn, #reset-btn, button")
    SUCCESS_MSG        = (By.CSS_SELECTOR,
                          ".success, .alert-success, [class*='success']")
    ERROR_MSG          = (By.CSS_SELECTOR,
                          ".error, .alert-danger, [class*='error']")
    LOGIN_LINK         = (By.CSS_SELECTOR,
                          "a[href*='login'], .login-link, .back-to-login")

    def open(self):
        return super().open("reset_password")

    def open_with_token(self, token: str):
        from automation.config.settings import PAGES
        url = PAGES["reset_password"] + f"?token={token}"
        return self.open_url(url)

    # ── Actions ───────────────────────────────────────────────────────────────
    def enter_new_password(self, pwd: str):
        self.type_text(*self.NEW_PWD_INPUT, pwd)
        return self

    def enter_confirm_password(self, pwd: str):
        self.type_text(*self.CONFIRM_PWD_INPUT, pwd)
        return self

    def click_submit(self):
        self.click(*self.SUBMIT_BTN)
        return self

    def reset_password(self, new_pwd: str, confirm_pwd: str = ""):
        self.enter_new_password(new_pwd)
        self.enter_confirm_password(confirm_pwd or new_pwd)
        self.click_submit()
        return self

    # ── Verifications ─────────────────────────────────────────────────────────
    def is_on_reset_page(self) -> bool:
        return "reset" in self.get_current_url().lower()

    def get_success_message(self) -> str:
        if self.is_visible(*self.SUCCESS_MSG, timeout=5):
            return self.get_text(*self.SUCCESS_MSG)
        return ""

    def get_error_message(self) -> str:
        if self.is_visible(*self.ERROR_MSG, timeout=5):
            return self.get_text(*self.ERROR_MSG)
        return ""

    def get_message(self) -> str:
        return self.get_success_message() or self.get_error_message()

    def is_new_pwd_field_visible(self) -> bool:
        return self.is_visible(*self.NEW_PWD_INPUT)

    def is_submit_btn_visible(self) -> bool:
        return self.is_visible(*self.SUBMIT_BTN)

    def has_login_link(self) -> bool:
        return self.is_present(*self.LOGIN_LINK)


# ─────────────────────────────────────────────────────────────────────────────
# WORKFLOW PAGE
# ─────────────────────────────────────────────────────────────────────────────

class WorkflowPage(BasePage):
    """Covers: /workflow.html"""

    # ── Locators ──────────────────────────────────────────────────────────────
    STEPS              = (By.CSS_SELECTOR,
                          ".step, .workflow-step, [class*='step'], "
                          "ol li, ul.steps li, .process-step")
    STEP_NUMBERS       = (By.CSS_SELECTOR,
                          ".step-number, .step-num, [class*='step-number']")
    STEP_TITLES        = (By.CSS_SELECTOR,
                          ".step-title, .step h3, .step h4, [class*='step-title']")
    STEP_DESCRIPTIONS  = (By.CSS_SELECTOR,
                          ".step-description, .step p, [class*='step-desc']")
    UPLOAD_LINK        = (By.CSS_SELECTOR,
                          "a[href*='upload'], button[class*='upload'], .start-btn")
    NEXT_BTN           = (By.CSS_SELECTOR,
                          ".next-btn, button[class*='next'], #next, a[class*='next']")
    BACK_BTN           = (By.CSS_SELECTOR,
                          ".back-btn, button[class*='back'], #back, a[class*='back']")
    PROGRESS_BAR       = (By.CSS_SELECTOR,
                          ".progress, .progress-bar, [role='progressbar'], [class*='progress']")
    MAIN_CONTENT       = (By.CSS_SELECTOR,
                          "main, .main-content, .workflow-container, .content")
    DIAGRAM            = (By.CSS_SELECTOR,
                          ".diagram, .flow-chart, svg, canvas, .workflow-diagram")
    HELP_SECTION       = (By.CSS_SELECTOR,
                          ".help, .faq, .instructions, [class*='help']")
    NAV_LINKS          = (By.CSS_SELECTOR,
                          "nav a, .navbar a, .sidebar a, .nav-link")

    def open(self):
        return super().open("workflow")

    def is_on_workflow_page(self) -> bool:
        return "workflow" in self.get_current_url().lower()

    def get_step_count(self) -> int:
        return self.element_count(*self.STEPS)

    def has_upload_link(self) -> bool:
        return self.is_present(*self.UPLOAD_LINK)

    def has_progress_indicator(self) -> bool:
        return self.is_present(*self.PROGRESS_BAR)

    def has_main_content(self) -> bool:
        return self.is_visible(*self.MAIN_CONTENT)

    def has_navigation(self) -> bool:
        return self.element_count(*self.NAV_LINKS) > 0

    def get_page_heading(self) -> str:
        if self.is_present(By.CSS_SELECTOR, "h1,h2"):
            return self.get_text(By.CSS_SELECTOR, "h1,h2")
        return ""

    def click_upload_link(self):
        if self.has_upload_link():
            self.click(*self.UPLOAD_LINK)
        return self


# ─────────────────────────────────────────────────────────────────────────────
# REFINE PAGE
# ─────────────────────────────────────────────────────────────────────────────

class RefinePage(BasePage):
    """Covers: /refine.html — adjust segmentation thresholds, re-analyze."""

    # ── Locators ──────────────────────────────────────────────────────────────
    THRESHOLD_SLIDER   = (By.CSS_SELECTOR,
                          "#threshold, input[type='range'][name*='threshold'], "
                          ".threshold-slider, input[type='range']:first-of-type")
    THRESHOLD_INPUT    = (By.CSS_SELECTOR,
                          "input[type='number'][name*='threshold'], "
                          "#threshold-value, .threshold-input")
    APPLY_BTN          = (By.CSS_SELECTOR,
                          "#apply-btn, button[id*='apply'], button[class*='apply'], "
                          "button[class*='refine'], .apply-btn")
    RESET_BTN          = (By.CSS_SELECTOR,
                          "#reset-btn, button[class*='reset'], .reset-btn, "
                          "button[id*='reset']")
    PREVIEW_CANVAS     = (By.CSS_SELECTOR,
                          "canvas, #preview-canvas, .preview-canvas, .stl-preview")
    REGION_CHECKBOXES  = (By.CSS_SELECTOR,
                          "input[type='checkbox'][name*='region'], "
                          ".region-checkbox, #region-select input")
    REGION_SELECTOR    = (By.CSS_SELECTOR,
                          "#region-select, select[name*='region'], .region-selector")
    LOADING_SPINNER    = (By.CSS_SELECTOR,
                          ".loading, .spinner, [class*='loading'], [class*='spinner']")
    SUCCESS_MSG        = (By.CSS_SELECTOR,
                          ".success, .alert-success, [class*='success']")
    ERROR_MSG          = (By.CSS_SELECTOR,
                          ".error, .alert-danger, [class*='error']")
    BACK_BTN           = (By.CSS_SELECTOR,
                          ".back-btn, a[href*='results'], button[class*='back']")
    STL_DOWNLOAD       = (By.CSS_SELECTOR,
                          ".download-btn, a[download], button[class*='download'], "
                          "a[href*='.stl']")
    CONTROLS_PANEL     = (By.CSS_SELECTOR,
                          ".controls, .controls-panel, .refine-controls, aside")

    def open(self):
        return super().open("refine")

    def is_on_refine_page(self) -> bool:
        return "refine" in self.get_current_url().lower()

    # ── Actions ───────────────────────────────────────────────────────────────
    def set_threshold(self, value: str):
        """Set threshold via the number input if present, else move slider."""
        if self.is_present(*self.THRESHOLD_INPUT):
            self.type_text(*self.THRESHOLD_INPUT, value)
        elif self.is_present(*self.THRESHOLD_SLIDER):
            slider = self.find(*self.THRESHOLD_SLIDER)
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; "
                "arguments[0].dispatchEvent(new Event('input')); "
                "arguments[0].dispatchEvent(new Event('change'));",
                slider, value,
            )
        return self

    def click_apply(self):
        if self.is_present(*self.APPLY_BTN):
            self.click(*self.APPLY_BTN)
        return self

    def click_reset(self):
        if self.is_present(*self.RESET_BTN):
            self.click(*self.RESET_BTN)
        return self

    def click_back(self):
        if self.is_present(*self.BACK_BTN):
            self.click(*self.BACK_BTN)
        return self

    def select_region(self, value: str):
        if self.is_present(*self.REGION_SELECTOR):
            from selenium.webdriver.support.ui import Select
            sel = Select(self.find(*self.REGION_SELECTOR))
            try:
                sel.select_by_value(value)
            except Exception:
                sel.select_by_visible_text(value)
        return self

    # ── Verifications ─────────────────────────────────────────────────────────
    def has_controls(self) -> bool:
        return (self.is_present(*self.CONTROLS_PANEL)
                or self.is_present(*self.THRESHOLD_SLIDER)
                or self.is_present(*self.APPLY_BTN))

    def has_preview(self) -> bool:
        return self.is_present(*self.PREVIEW_CANVAS)

    def has_download_btn(self) -> bool:
        return self.is_present(*self.STL_DOWNLOAD)

    def is_loading(self) -> bool:
        return self.is_visible(*self.LOADING_SPINNER, timeout=2)

    def get_success_message(self) -> str:
        if self.is_visible(*self.SUCCESS_MSG, timeout=5):
            return self.get_text(*self.SUCCESS_MSG)
        return ""

    def get_error_message(self) -> str:
        if self.is_visible(*self.ERROR_MSG, timeout=5):
            return self.get_text(*self.ERROR_MSG)
        return ""
