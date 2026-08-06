"""
Dashboard Page Object Model
"""
from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage


class DashboardPage(BasePage):
    NAV_LINKS       = (By.CSS_SELECTOR, "nav a, .navbar a, .sidebar a")
    LOGOUT_BTN      = (By.CSS_SELECTOR, ".logout, #logout, a[href*='logout'], button[class*='logout']")
    UPLOAD_BTN      = (By.CSS_SELECTOR, "a[href*='upload'], .upload-btn, button[class*='upload']")
    HISTORY_LINK    = (By.CSS_SELECTOR, "a[href*='history'], .history-link")
    WELCOME_MSG     = (By.CSS_SELECTOR, ".welcome, .user-name, .greeting, h1, h2")
    SCAN_COUNT      = (By.CSS_SELECTOR, ".scan-count, .total-scans, [class*='count']")
    RECENT_SCANS    = (By.CSS_SELECTOR, ".recent-scans, .scan-list, .scan-item, tbody tr")
    STATS_CARDS     = (By.CSS_SELECTOR, ".stat-card, .card, .dashboard-card, .metric-card")
    HEADER          = (By.CSS_SELECTOR, "header, .header, .top-nav, .navbar")
    FOOTER          = (By.CSS_SELECTOR, "footer, .footer")
    PROFILE_ICON    = (By.CSS_SELECTOR, ".profile-icon, .user-avatar, .profile-btn")
    SIDEBAR         = (By.CSS_SELECTOR, ".sidebar, .side-nav, aside")
    MAIN_CONTENT    = (By.CSS_SELECTOR, "main, .main-content, .content, #main")
    LOGO            = (By.CSS_SELECTOR, ".logo, .brand, img[alt*='logo' i]")
    NOTIFICATION    = (By.CSS_SELECTOR, ".notification, .alert, .toast")

    def open(self):
        return super().open("dashboard")

    def is_on_dashboard(self) -> bool:
        return "dashboard" in self.get_current_url().lower()

    def click_logout(self):
        self.click(*self.LOGOUT_BTN); return self

    def click_upload(self):
        self.click(*self.UPLOAD_BTN); return self

    def click_history(self):
        self.click(*self.HISTORY_LINK); return self

    def get_welcome_text(self) -> str:
        if self.is_visible(*self.WELCOME_MSG, timeout=5):
            return self.get_text(*self.WELCOME_MSG)
        return ""

    def nav_links_count(self) -> int:
        return self.element_count(*self.NAV_LINKS)

    def is_header_visible(self) -> bool:
        return self.is_visible(*self.HEADER)

    def is_footer_visible(self) -> bool:
        return self.is_visible(*self.FOOTER)

    def get_stats_count(self) -> int:
        return self.element_count(*self.STATS_CARDS)

    def recent_scans_count(self) -> int:
        return self.element_count(*self.RECENT_SCANS)

    def is_logo_visible(self) -> bool:
        return self.is_visible(*self.LOGO)

    def get_page_load_time(self) -> float:
        timing = self.driver.execute_script(
            "var t=window.performance.timing;"
            "return t.loadEventEnd - t.navigationStart;"
        )
        return timing / 1000.0


class UploadPage(BasePage):
    FILE_INPUT      = (By.CSS_SELECTOR, "input[type='file'], #file-upload, .file-input")
    PATIENT_NAME    = (By.CSS_SELECTOR, "input[name='patient_name'], #patient-name, input[placeholder*='patient' i]")
    UPLOAD_BTN      = (By.CSS_SELECTOR, "button[type='submit'], .upload-btn, #upload-btn, button")
    PROGRESS_BAR    = (By.CSS_SELECTOR, ".progress, .progress-bar, [role='progressbar']")
    SUCCESS_MSG     = (By.CSS_SELECTOR, ".success, .alert-success, [class*='success']")
    ERROR_MSG       = (By.CSS_SELECTOR, ".error, .alert-danger, [class*='error']")
    DRAG_DROP_ZONE  = (By.CSS_SELECTOR, ".drop-zone, .drag-drop, [class*='drag']")
    SUPPORTED_TYPES = (By.CSS_SELECTOR, ".supported-types, .file-types, [class*='accept']")

    def open(self):
        return super().open("upload")

    def is_on_upload_page(self) -> bool:
        return "upload" in self.get_current_url().lower()

    def is_file_input_present(self) -> bool:
        return self.is_present(*self.FILE_INPUT)

    def is_upload_btn_visible(self) -> bool:
        return self.is_visible(*self.UPLOAD_BTN)


class ForgotPasswordPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'], input[name='email'], #email")
    SUBMIT_BTN  = (By.CSS_SELECTOR, "button[type='submit'], .submit-btn, button")
    SUCCESS_MSG = (By.CSS_SELECTOR, ".success, .alert-success, [class*='success']")
    ERROR_MSG   = (By.CSS_SELECTOR, ".error, .alert-danger, [class*='error']")
    LOGIN_LINK  = (By.CSS_SELECTOR, "a[href*='login']")

    def open(self):
        return super().open("forgot_password")

    def submit_email(self, email: str):
        self.open()
        self.type_text(*self.EMAIL_INPUT, email)
        self.click(*self.SUBMIT_BTN)
        return self

    def get_message(self) -> str:
        for loc in [self.SUCCESS_MSG, self.ERROR_MSG]:
            if self.is_visible(*loc, timeout=4):
                return self.get_text(*loc)
        return ""
