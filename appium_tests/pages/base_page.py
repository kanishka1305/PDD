"""
DentAI Appium — Base Page
==========================
All page objects inherit from BasePage.
Provides shared helpers: explicit waits, element finders, screenshots, scrolling.

Locator strategy for React Native (no testID props in source):
  1. ANDROID_UIAUTOMATOR  text()  — primary for visible text
  2. XPATH with class     — for EditText inputs, generic views
  3. ACCESSIBILITY_ID     — where available
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from appium_tests.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from appium_tests.config.config import (
    EXPLICIT_WAIT,
    PAGE_LOAD_WAIT,
    SCREENSHOTS_DIR,
)

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all page objects.
    Wraps Appium driver with reusable helpers and explicit waits.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, EXPLICIT_WAIT)
        self.long_wait = WebDriverWait(driver, PAGE_LOAD_WAIT)

    # ── Locator helpers ────────────────────────────────────────────────────────

    def _by_text(self, text: str):
        """Return (by, value) tuple for UIAutomator exact text match."""
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{text}")',
        )

    def _by_text_contains(self, text: str):
        """Return (by, value) for UIAutomator text contains."""
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{text}")',
        )

    def _by_xpath(self, xpath: str):
        return AppiumBy.XPATH, xpath

    def _by_class(self, cls: str):
        return AppiumBy.CLASS_NAME, cls

    def _by_acc_id(self, acc_id: str):
        return AppiumBy.ACCESSIBILITY_ID, acc_id

    def _nth_edit_text(self, n: int):
        """Return XPath for the nth EditText on screen (1-indexed)."""
        return AppiumBy.XPATH, f"(//android.widget.EditText)[{n}]"

    # ── Wait helpers ───────────────────────────────────────────────────────────

    def wait_for_text(self, text: str, timeout: int = EXPLICIT_WAIT):
        """Wait until an element with the exact text is visible."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR,
                     f'new UiSelector().text("{text}")')
                )
            )
        except TimeoutException:
            logger.warning("Timed out waiting for text: '%s'", text)
            raise

    def wait_for_text_contains(self, text: str, timeout: int = EXPLICIT_WAIT):
        """Wait until an element containing the text is visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR,
                 f'new UiSelector().textContains("{text}")')
            )
        )

    def wait_for_element_gone(self, text: str, timeout: int = EXPLICIT_WAIT):
        """Wait until an element with exact text is no longer visible."""
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR,
                     f'new UiSelector().text("{text}")')
                )
            )
        except TimeoutException:
            pass  # Already gone or never appeared

    # ── Find helpers ───────────────────────────────────────────────────────────

    def find_by_text(self, text: str):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{text}")',
        )

    def find_by_text_contains(self, text: str):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{text}")',
        )

    def find_nth_edit_text(self, n: int):
        return self.driver.find_element(
            AppiumBy.XPATH, f"(//android.widget.EditText)[{n}]"
        )

    def is_text_visible(self, text: str, timeout: int = 5) -> bool:
        """Return True if an element with exact text is visible within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR,
                     f'new UiSelector().text("{text}")')
                )
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_text_contains_visible(self, text: str, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR,
                     f'new UiSelector().textContains("{text}")')
                )
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # ── Action helpers ─────────────────────────────────────────────────────────

    def tap_text(self, text: str) -> None:
        """Wait for and tap an element by exact text."""
        el = self.wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR,
                 f'new UiSelector().text("{text}")')
            )
        )
        el.click()
        logger.debug("Tapped: '%s'", text)

    def type_into_field(self, n: int, value: str, clear: bool = True) -> None:
        """
        Type into the nth EditText on screen.

        Args:
            n: 1-indexed EditText position.
            value: Text to type.
            clear: Clear existing content before typing.
        """
        el = self.wait.until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, f"(//android.widget.EditText)[{n}]")
            )
        )
        if clear:
            el.clear()
        el.send_keys(value)
        logger.debug("Typed into field[%d]: '%s'", n, value[:20] + "..." if len(value) > 20 else value)

    def scroll_down(self) -> None:
        """Scroll down by swiping up on screen."""
        size   = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.75)
        end_y   = int(size["height"] * 0.25)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def scroll_up(self) -> None:
        size   = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.25)
        end_y   = int(size["height"] * 0.75)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def scroll_to_text(self, text: str) -> None:
        """Scroll until an element with the given text is visible."""
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().text("{text}"))',
            )
        except Exception:
            logger.warning("Could not scroll to text: '%s'", text)

    def hide_keyboard(self) -> None:
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def get_current_activity(self) -> str:
        try:
            return self.driver.current_activity
        except Exception:
            return ""

    def short_sleep(self, seconds: float = 0.5) -> None:
        time.sleep(seconds)

    # ── Screenshot ─────────────────────────────────────────────────────────────

    def take_screenshot(self, name: str = "") -> Optional[str]:
        """
        Capture a screenshot and save to reports/screenshots/.

        Returns:
            Absolute path to the saved screenshot, or None on failure.
        """
        try:
            ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"{name}_{ts}.png" if name else f"screenshot_{ts}.png"
            path  = SCREENSHOTS_DIR / fname
            self.driver.save_screenshot(str(path))
            logger.info("Screenshot saved: %s", path)
            return str(path)
        except Exception as exc:
            logger.error("Screenshot failed: %s", exc)
            return None

    # ── App state ──────────────────────────────────────────────────────────────

    def reset_app(self) -> None:
        """Terminate and relaunch the app (equivalent to fresh start)."""
        try:
            from appium_tests.config.config import APP_PACKAGE
            self.driver.terminate_app(APP_PACKAGE)
            time.sleep(1)
            self.driver.activate_app(APP_PACKAGE)
            time.sleep(2)
        except Exception as exc:
            logger.warning("reset_app failed: %s", exc)
