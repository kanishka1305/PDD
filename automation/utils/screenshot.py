"""
Screenshot utility — captures and stores screenshots.
"""
import base64
from datetime import datetime
from pathlib import Path
from automation.config.settings import SCREENSHOT_DIR
from automation.utils.logger import log


def take_screenshot(driver, name: str) -> Path:
    """Capture a screenshot and save it. Returns the file path."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = name.replace(" ", "_").replace("/", "_").replace(":", "")[:80]
    path = SCREENSHOT_DIR / f"{safe_name}_{ts}.png"
    try:
        driver.save_screenshot(str(path))
        log.info("Screenshot saved: %s", path.name)
    except Exception as exc:
        log.warning("Screenshot failed for '%s': %s", name, exc)
    return path


def get_screenshot_base64(driver) -> str:
    """Return a base64-encoded PNG screenshot for embedding in HTML."""
    try:
        return driver.get_screenshot_as_base64()
    except Exception:
        return ""


def take_full_page_screenshot(driver, name: str) -> Path:
    """Scroll and stitch a full-page screenshot (Chrome CDP)."""
    try:
        original_size = driver.get_window_size()
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, max(scroll_height, 900))
        path = take_screenshot(driver, f"fullpage_{name}")
        driver.set_window_size(original_size["width"], original_size["height"])
        return path
    except Exception:
        return take_screenshot(driver, name)
