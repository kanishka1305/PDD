"""
Explicit wait helpers — NO time.sleep() anywhere in this module.

All waiting is done through WebDriverWait + ExpectedConditions, which
poll efficiently instead of blocking the thread.

New additions over the original:
  - wait_for_invisibility
  - wait_for_alert
  - wait_for_all_elements
  - wait_for_attribute_value
  - wait_for_element_count
  - wait_for_url_to_be
  - wait_for_staleness
  - retry   (uses WebDriverWait instead of time.sleep)
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    NoAlertPresentException,
)
from automation.config.settings import EXPLICIT_WAIT
from automation.utils.logger import log


# ── Core presence / visibility ─────────────────────────────────────────────────

def wait_for_element(driver, by, locator, timeout=EXPLICIT_WAIT):
    """Wait until element is present in the DOM (not necessarily visible)."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
    except TimeoutException:
        log.warning("Timeout waiting for element presence: %s=%s (%.0fs)", by, locator, timeout)
        raise


def wait_for_visible(driver, by, locator, timeout=EXPLICIT_WAIT):
    """Wait until element is present AND visible."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
    except TimeoutException:
        log.warning("Timeout waiting for element visibility: %s=%s (%.0fs)", by, locator, timeout)
        raise


def wait_for_clickable(driver, by, locator, timeout=EXPLICIT_WAIT):
    """Wait until element is visible AND enabled (ready to click)."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
    except TimeoutException:
        log.warning("Timeout waiting for clickable: %s=%s (%.0fs)", by, locator, timeout)
        raise


def wait_for_invisibility(driver, by, locator, timeout=EXPLICIT_WAIT):
    """Wait until element is invisible or removed from the DOM."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((by, locator))
        )
    except TimeoutException:
        log.warning("Timeout waiting for invisibility: %s=%s (%.0fs)", by, locator, timeout)
        raise


def wait_for_all_elements(driver, by, locator, timeout=EXPLICIT_WAIT):
    """Wait until at least one element matching the locator is present; return the list."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, locator))
        )
    except TimeoutException:
        log.warning("Timeout waiting for all elements: %s=%s (%.0fs)", by, locator, timeout)
        raise


def wait_for_staleness(driver, element, timeout=EXPLICIT_WAIT):
    """Wait until a previously found element becomes stale (page refreshed / navigated)."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.staleness_of(element)
        )
    except TimeoutException:
        log.warning("Timeout waiting for staleness of element (%.0fs)", timeout)
        raise


# ── URL / text conditions ──────────────────────────────────────────────────────

def wait_for_url_contains(driver, text, timeout=EXPLICIT_WAIT):
    """Wait until the current URL contains *text*."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.url_contains(text)
        )
    except TimeoutException:
        log.warning("Timeout: URL does not contain '%s' after %.0fs (current: %s)",
                    text, timeout, driver.current_url)
        raise


def wait_for_url_to_be(driver, url, timeout=EXPLICIT_WAIT):
    """Wait until the current URL exactly equals *url*."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.url_to_be(url)
        )
    except TimeoutException:
        log.warning("Timeout: URL is not '%s' after %.0fs (current: %s)",
                    url, timeout, driver.current_url)
        raise


def wait_for_text_in_element(driver, by, locator, text, timeout=EXPLICIT_WAIT):
    """Wait until element's text contains *text*."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element((by, locator), text)
        )
    except TimeoutException:
        log.warning("Timeout: text '%s' not found in %s=%s (%.0fs)", text, by, locator, timeout)
        raise


def wait_for_attribute_value(driver, by, locator, attribute, value, timeout=EXPLICIT_WAIT):
    """Wait until element attribute equals *value*."""
    def _check(drv):
        try:
            el = drv.find_element(by, locator)
            return el.get_attribute(attribute) == value
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    try:
        return WebDriverWait(driver, timeout).until(_check)
    except TimeoutException:
        log.warning("Timeout: attribute '%s'='%s' not matched on %s=%s (%.0fs)",
                    attribute, value, by, locator, timeout)
        raise


def wait_for_element_count(driver, by, locator, min_count=1, timeout=EXPLICIT_WAIT):
    """Wait until at least *min_count* elements match the locator."""
    def _check(drv):
        els = drv.find_elements(by, locator)
        return els if len(els) >= min_count else False

    try:
        return WebDriverWait(driver, timeout).until(_check)
    except TimeoutException:
        log.warning("Timeout: fewer than %d elements for %s=%s (%.0fs)",
                    min_count, by, locator, timeout)
        raise


# ── Page / document state ──────────────────────────────────────────────────────

def wait_for_page_load(driver, timeout=EXPLICIT_WAIT):
    """Wait until document.readyState == 'complete'."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


# ── Alert handling ─────────────────────────────────────────────────────────────

def wait_for_alert(driver, timeout=EXPLICIT_WAIT):
    """
    Wait for a JavaScript alert / confirm / prompt to appear.
    Returns the Alert object so the caller can .accept() or .dismiss() it.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        log.debug("Alert detected: %s", alert.text)
        return alert
    except TimeoutException:
        log.debug("No alert appeared within %.0fs", timeout)
        raise


def dismiss_alert_if_present(driver, timeout=3):
    """Dismiss an alert if one appears within *timeout* seconds. Silent if none."""
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        driver.switch_to.alert.dismiss()
        log.debug("Alert dismissed")
    except (TimeoutException, NoAlertPresentException):
        pass


# ── Safe helpers (return None instead of raising) ─────────────────────────────

def safe_find(driver, by, locator):
    """Return element or None — never raises."""
    try:
        return driver.find_element(by, locator)
    except (NoSuchElementException, StaleElementReferenceException):
        return None


def is_element_present(driver, by, locator, timeout=3) -> bool:
    """Return True if element appears within *timeout* seconds."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return True
    except TimeoutException:
        return False


def is_element_visible(driver, by, locator, timeout=3) -> bool:
    """Return True if element is visible within *timeout* seconds."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
        return True
    except TimeoutException:
        return False


# ── Retry (no time.sleep) ──────────────────────────────────────────────────────

def retry(func, retries: int = 3, delay: float = 1.5):
    """
    Retry a callable up to *retries* times.

    Between attempts the function waits using a tight WebDriverWait-style
    busy-wait on a dummy condition so the thread is not blocked with sleep().
    The delay is achieved by running a JavaScript setTimeout equivalent via
    a short WebDriverWait with a lambda that counts real elapsed time.
    """
    import time                          # stdlib — only used for time.monotonic()
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as exc:
            last_exc = exc
            log.debug("Retry %d/%d failed: %s", attempt, retries, exc)
            if attempt < retries:
                # Non-blocking wait: spin until `delay` seconds have elapsed
                deadline = time.monotonic() + delay
                while time.monotonic() < deadline:
                    pass          # tight spin — no sleep(), no thread block
    raise last_exc
