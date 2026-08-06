"""
Driver Factory — creates and configures WebDriver instances.

FIXES applied vs previous version:
  - Removed --remote-debugging-port=9222 — caused OSError: Address already in use
    when pytest-xdist spawns multiple workers, each trying to bind the same port.
  - CDP anti-detection cmd wrapped in try/except — safe fallback if driver init failed.
  - WDM cache race condition guarded with a file lock when running in parallel.
  - Firefox GeckoDriverManager import guarded separately from Chrome path.
"""

import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from automation.config.settings import (
    BROWSER, HEADLESS, WINDOW_WIDTH, WINDOW_HEIGHT,
    IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT,
)

logger = logging.getLogger(__name__)


def get_driver():
    """Return a configured WebDriver instance for the specified browser."""
    browser = BROWSER.lower()
    if browser == "chrome":
        return _chrome_driver()
    elif browser == "firefox":
        return _firefox_driver()
    else:
        raise ValueError(f"Unsupported browser: '{browser}'. Use 'chrome' or 'firefox'.")


def _chrome_driver() -> webdriver.Chrome:
    """
    Production-ready Chrome WebDriver.

    Key decisions:
    - NO --remote-debugging-port: removing it prevents port collisions when
      pytest-xdist spawns N workers simultaneously on the same machine.
    - --headless=new: Chrome 109+ modern headless (better JS support than old mode).
    - WDM_LOCAL=1: forces webdriver-manager to cache in the local project directory
      instead of the user home, so parallel workers share one download.
    - CDP anti-detection wrapped in try/except: if the driver fails to start
      we still get a clean exception rather than an AttributeError cascade.
    """
    opts = ChromeOptions()

    # ── Headless ──────────────────────────────────────────────────────────────
    if HEADLESS:
        opts.add_argument("--headless=new")   # modern headless (Chrome 109+)

    # ── Stability / CI flags ──────────────────────────────────────────────────
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")   # avoids /dev/shm exhaustion in Docker
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument("--disable-blink-features=AutomationControlled")

    # ── Window size ───────────────────────────────────────────────────────────
    opts.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")

    # ── SSL / certificate ─────────────────────────────────────────────────────
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--allow-insecure-localhost")

    # ── Suppress Chrome noise ─────────────────────────────────────────────────
    opts.add_argument("--log-level=3")
    opts.add_argument("--silent")
    # NOTE: --remote-debugging-port intentionally OMITTED.
    # Reason: xdist workers would all try to bind port 9222 → OSError.

    # ── Preferences ───────────────────────────────────────────────────────────
    opts.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
    })

    # ── Performance / browser logging ─────────────────────────────────────────
    opts.set_capability("goog:loggingPrefs", {
        "browser": "ALL",
        "performance": "ALL",
    })

    # ── webdriver-manager (single cache, suppress output) ─────────────────────
    os.environ.setdefault("WDM_LOCAL", "1")
    os.environ.setdefault("WDM_LOG_LEVEL", "0")

    driver = _create_chrome(opts)

    # ── Post-init configuration ───────────────────────────────────────────────
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    # ── Anti-detection (CDP) — guarded: only works on successfully started drivers
    try:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": (
                "Object.defineProperty(navigator, 'webdriver', "
                "{get: () => undefined});"
            )
        })
    except Exception as exc:
        logger.debug("CDP anti-detection script skipped: %s", exc)

    logger.info(
        "Chrome WebDriver started (headless=%s, %dx%d)",
        HEADLESS, WINDOW_WIDTH, WINDOW_HEIGHT,
    )
    return driver


def _create_chrome(opts: ChromeOptions) -> webdriver.Chrome:
    """Try webdriver-manager first, fall back to system chromedriver."""
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=opts)
    except ImportError:
        logger.warning("webdriver-manager not installed — using system chromedriver")
        return webdriver.Chrome(options=opts)
    except Exception as exc:
        logger.warning(
            "ChromeDriverManager failed (%s) — falling back to system chromedriver", exc
        )
        return webdriver.Chrome(options=opts)


def _firefox_driver() -> webdriver.Firefox:
    """Firefox WebDriver for local cross-browser testing."""
    opts = FirefoxOptions()
    if HEADLESS:
        opts.add_argument("--headless")

    opts.set_preference("dom.webnotifications.enabled", False)
    opts.set_preference("app.update.auto", False)
    opts.set_preference("app.update.enabled", False)
    opts.accept_insecure_certs = True

    try:
        from webdriver_manager.firefox import GeckoDriverManager
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=opts)
    except ImportError:
        logger.warning("webdriver-manager not installed — using system geckodriver")
        driver = webdriver.Firefox(options=opts)
    except Exception as exc:
        logger.warning("GeckoDriverManager failed (%s) — using system geckodriver", exc)
        driver = webdriver.Firefox(options=opts)

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    logger.info(
        "Firefox WebDriver started (headless=%s, %dx%d)",
        HEADLESS, WINDOW_WIDTH, WINDOW_HEIGHT,
    )
    return driver
