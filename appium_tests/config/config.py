"""
DentAI Mobile — Appium Configuration
=====================================
All capabilities read from environment variables.
No hardcoded credentials or device-specific values.

Environment variables:
  APPIUM_SERVER_URL        Appium server URL           (default: http://localhost:4723)
  ANDROID_DEVICE_NAME      Device/emulator name        (default: emulator-5554)
  ANDROID_PLATFORM_VERSION Android version             (default: 14)
  APP_PATH                 Path to debug APK           (default: see below)
  TEST_EMAIL               Test account email          (default: appiumtest@dentai.com)
  TEST_PASSWORD            Test account password       (default: AppiumTest@123)
  APPIUM_TIMEOUT           Implicit wait seconds       (default: 10)
  APPIUM_EXPLICIT_WAIT     Explicit wait max seconds   (default: 20)
"""

import os
from pathlib import Path

# ── Repository root ────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).parent.parent.parent

# ── Appium server ──────────────────────────────────────────────────────────────
APPIUM_SERVER_URL: str = os.environ.get(
    "APPIUM_SERVER_URL", "http://localhost:4723"
)

# ── Android device ─────────────────────────────────────────────────────────────
ANDROID_DEVICE_NAME: str = os.environ.get(
    "ANDROID_DEVICE_NAME", "emulator-5554"
)
ANDROID_PLATFORM_VERSION: str = os.environ.get(
    "ANDROID_PLATFORM_VERSION", "14"
)
ANDROID_AUTOMATION_NAME: str = "UiAutomator2"

# ── Application ────────────────────────────────────────────────────────────────
APP_PACKAGE: str  = "com.dentaimobile"
APP_ACTIVITY: str = "com.dentaimobile.MainActivity"

# Default APK path (built from source; override with APP_PATH env var)
_DEFAULT_APK = str(
    _REPO_ROOT
    / "DentAI-Mobile"
    / "android"
    / "app"
    / "build"
    / "outputs"
    / "apk"
    / "debug"
    / "app-debug.apk"
)
APP_PATH: str = os.environ.get("APP_PATH", _DEFAULT_APK)

# ── Timeouts ───────────────────────────────────────────────────────────────────
IMPLICIT_WAIT: int   = int(os.environ.get("APPIUM_TIMEOUT",        "10"))
EXPLICIT_WAIT: int   = int(os.environ.get("APPIUM_EXPLICIT_WAIT",  "20"))
PAGE_LOAD_WAIT: int  = 30    # seconds to wait for a new screen to appear
SEGMENTATION_WAIT: int = 180  # AI segmentation can take up to 3 minutes

# ── Test credentials ───────────────────────────────────────────────────────────
# Never hardcoded in tests — always read from env / GitHub Secrets
TEST_EMAIL: str    = os.environ.get("TEST_EMAIL",    "appiumtest@dentai.com")
TEST_PASSWORD: str = os.environ.get("TEST_PASSWORD", "AppiumTest@123")
TEST_NAME: str     = os.environ.get("TEST_NAME",     "Appium Test Doctor")
TEST_LICENSE: str  = os.environ.get("TEST_LICENSE",  "AT-000001")

# ── Test data ──────────────────────────────────────────────────────────────────
# Path to a sample DICOM file for upload tests
# Set DICOM_FILE_PATH env var to point at your test file
DICOM_FILE_PATH: str = os.environ.get(
    "DICOM_FILE_PATH",
    str(_REPO_ROOT / "appium_tests" / "test_data" / "sample.dcm"),
)

# ── Backend API ────────────────────────────────────────────────────────────────
BASE_URL: str = os.environ.get("BASE_URL", "https://pdd-uw63.onrender.com")

# ── Report paths ───────────────────────────────────────────────────────────────
APPIUM_DIR   = Path(__file__).parent.parent
REPORTS_DIR  = APPIUM_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
LOGS_DIR        = REPORTS_DIR / "logs"
HTML_DIR        = REPORTS_DIR / "html"
EXCEL_DIR       = REPORTS_DIR / "excel"
VIDEOS_DIR      = REPORTS_DIR / "videos"

# Ensure directories exist at import time
for _d in (SCREENSHOTS_DIR, LOGS_DIR, HTML_DIR, EXCEL_DIR, VIDEOS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ── Desired capabilities ───────────────────────────────────────────────────────
def get_capabilities(install_app: bool = True) -> dict:
    """
    Return Appium desired capabilities dict.

    Args:
        install_app: If True, always reinstall the APK before the session.
                     Set False when the APK is already installed.
    """
    caps: dict = {
        "platformName":         "Android",
        "appium:platformVersion": ANDROID_PLATFORM_VERSION,
        "appium:deviceName":    ANDROID_DEVICE_NAME,
        "appium:automationName": ANDROID_AUTOMATION_NAME,
        "appium:appPackage":    APP_PACKAGE,
        "appium:appActivity":   APP_ACTIVITY,
        "appium:noReset":       False,
        "appium:fullReset":     False,
        "appium:newCommandTimeout": 120,
        "appium:uiautomator2ServerInstallTimeout": 60000,
        "appium:adbExecTimeout": 60000,
        # React Native bridge wait
        "appium:androidInstallTimeout": 90000,
        # Auto-grant permissions (camera, storage, etc.)
        "appium:autoGrantPermissions": True,
    }

    if install_app and Path(APP_PATH).exists():
        caps["appium:app"] = APP_PATH
    else:
        # APK already installed — just launch by package + activity
        caps["appium:appPackage"]  = APP_PACKAGE
        caps["appium:appActivity"] = APP_ACTIVITY

    return caps
