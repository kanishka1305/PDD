"""
BasePage — parent class for all Page Objects.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from automation.utils.waits import (
    wait_for_element, wait_for_clickable,
    wait_for_visible, wait_for_page_load, safe_find
)
from automation.utils.screenshot import take_screenshot
from automation.utils.logger import log
from automation.config.settings import EXPLICIT_WAIT, PAGES


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    # ── Navigation ────────────────────────────────────────────────────────────
    def open(self, page_key: str):
        url = PAGES.get(page_key, page_key)
        log.info("Opening page: %s → %s", page_key, url)
        self.driver.get(url)
        wait_for_page_load(self.driver)
        return self

    def open_url(self, url: str):
        log.info("Opening URL: %s", url)
        self.driver.get(url)
        wait_for_page_load(self.driver)
        return self

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    # ── Element interactions ──────────────────────────────────────────────────
    def find(self, by, locator, timeout=EXPLICIT_WAIT):
        return wait_for_element(self.driver, by, locator, timeout)

    def find_visible(self, by, locator, timeout=EXPLICIT_WAIT):
        return wait_for_visible(self.driver, by, locator, timeout)

    def click(self, by, locator, timeout=EXPLICIT_WAIT):
        el = wait_for_clickable(self.driver, by, locator, timeout)
        el.click()
        return self

    def type_text(self, by, locator, text: str, clear_first=True):
        el = wait_for_visible(self.driver, by, locator)
        if clear_first:
            el.clear()
        el.send_keys(text)
        return self

    def get_text(self, by, locator) -> str:
        return self.find(by, locator).text.strip()

    def get_attribute(self, by, locator, attr: str) -> str:
        return self.find(by, locator).get_attribute(attr) or ""

    def is_visible(self, by, locator, timeout=5) -> bool:
        try:
            wait_for_visible(self.driver, by, locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_present(self, by, locator, timeout=3) -> bool:
        return safe_find(self.driver, by, locator) is not None

    def element_count(self, by, locator) -> int:
        return len(self.driver.find_elements(by, locator))

    # ── JS helpers ────────────────────────────────────────────────────────────
    def scroll_to(self, by, locator):
        el = self.find(by, locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        return self

    def js_click(self, by, locator):
        el = self.find(by, locator)
        self.driver.execute_script("arguments[0].click();", el)
        return self

    def get_page_source(self) -> str:
        return self.driver.page_source

    def get_console_logs(self) -> list:
        try:
            return self.driver.get_log("browser")
        except Exception:
            return []

    # ── Screenshot ────────────────────────────────────────────────────────────
    def screenshot(self, name: str):
        take_screenshot(self.driver, name)
        return self

    # ── Assertions ────────────────────────────────────────────────────────────
    def assert_url_contains(self, text: str):
        assert text in self.get_current_url(), \
            f"URL '{self.get_current_url()}' does not contain '{text}'"

    def assert_title_contains(self, text: str):
        assert text.lower() in self.get_title().lower(), \
            f"Title '{self.get_title()}' does not contain '{text}'"

    def assert_element_visible(self, by, locator):
        assert self.is_visible(by, locator), \
            f"Element {by}={locator} is not visible"

    def assert_text_contains(self, by, locator, text: str):
        actual = self.get_text(by, locator)
        assert text.lower() in actual.lower(), \
            f"Text '{actual}' does not contain '{text}'"
