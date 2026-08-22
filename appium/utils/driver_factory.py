"""
DentAI Appium — Driver Factory
================================
Creates and configures the Appium WebDriver session.
Supports real Android device and emulator.
"""

import logging
from appium import webdriver
from appium.options import AppiumOptions
from appium.webdriver.appium_service import AppiumService

from appium.config.config import (
    APPIUM_SERVER_URL,
    IMPLICIT_WAIT,
    get_capabilities,
)

logger = logging.getLogger(__name__)


def create_driver(install_app: bool = True) -> webdriver.Remote:
    """
    Create and return an Appium Remote WebDriver session.

    Args:
        install_app: Whether to install/reinstall the APK.

    Returns:
        Configured Appium WebDriver instance.

    Raises:
        Exception: If Appium server is unreachable or capabilities are invalid.
    """
    caps = get_capabilities(install_app=install_app)

    options = AppiumOptions()
    for key, value in caps.items():
        options.set_capability(key, value)

    logger.info("Connecting to Appium server: %s", APPIUM_SERVER_URL)
    logger.info("Device: %s | Platform: Android %s",
                caps.get("appium:deviceName"),
                caps.get("appium:platformVersion"))

    try:
        driver = webdriver.Remote(
            command_executor=APPIUM_SERVER_URL,
            options=options,
        )
        driver.implicitly_wait(IMPLICIT_WAIT)
        logger.info("Driver created successfully. Session ID: %s", driver.session_id)
        return driver

    except Exception as exc:
        logger.error("Failed to create Appium driver: %s", exc)
        raise


def quit_driver(driver: webdriver.Remote | None) -> None:
    """Safely quit the Appium driver session."""
    if driver is not None:
        try:
            driver.quit()
            logger.info("Driver session closed.")
        except Exception as exc:
            logger.warning("Error closing driver: %s", exc)
