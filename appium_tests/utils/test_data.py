"""
DentAI Appium — Centralized Test Data
=======================================
All test data in one place. Sensitive values read from env vars / GitHub Secrets.
Never import test data directly into individual test files.
"""

import os
from pathlib import Path

# ── Authentication ─────────────────────────────────────────────────────────────
VALID_EMAIL: str    = os.environ.get("TEST_EMAIL",    "appiumtest@dentai.com")
VALID_PASSWORD: str = os.environ.get("TEST_PASSWORD", "AppiumTest@123")
VALID_NAME: str     = os.environ.get("TEST_NAME",     "Appium Test Doctor")
VALID_LICENSE: str  = os.environ.get("TEST_LICENSE",  "AT-000001")

# ── Invalid credential sets (for negative tests) ───────────────────────────────
INVALID_EMAIL: str    = "notauser@nowhere.com"
INVALID_PASSWORD: str = "WrongPass999!"
EMPTY_EMAIL: str      = ""
EMPTY_PASSWORD: str   = ""

# Registration — uses a unique-ish email to avoid conflicts on reruns
import time as _time
REG_EMAIL: str    = os.environ.get(
    "REG_EMAIL", f"autotest_{int(_time.time())}@dentai.com"
)
REG_PASSWORD: str = os.environ.get("REG_PASSWORD", "AutoTest@2026!")
REG_NAME: str     = os.environ.get("REG_NAME",     "AutoReg Doctor")
REG_LICENSE: str  = os.environ.get("REG_LICENSE",  "AR-999999")

# ── File upload ────────────────────────────────────────────────────────────────
_APPIUM_DIR = Path(__file__).parent.parent
SAMPLE_DCM_PATH: str = os.environ.get(
    "DICOM_FILE_PATH",
    str(_APPIUM_DIR / "test_data" / "sample.dcm"),
)
SAMPLE_NII_PATH: str = os.environ.get(
    "NII_FILE_PATH",
    str(_APPIUM_DIR / "test_data" / "sample.nii"),
)

# ── Expected UI text (verified against actual source code) ────────────────────
class UIText:
    """Text strings verified against source code — do NOT change."""
    # Login screen
    BRAND_NAME            = "DentAI"
    BRAND_SUBTITLE        = "CBCT AI Segmentation Platform"
    LOGIN_HEADING         = "Welcome back"
    LOGIN_SUBHEADING      = "Sign in to your clinical account"
    SIGN_IN_BTN           = "Sign In"
    FORGOT_PASSWORD_LINK  = "Forgot password?"
    CREATE_ACCOUNT_LINK   = "Create account"

    # Signup screen
    SIGNUP_HEADING        = "Create your account"
    CREATE_ACCOUNT_BTN    = "Create Account"
    SIGNUP_SUCCESS        = "Account created!"

    # Dashboard screen
    CLINICAL_OVERVIEW     = "Clinical overview"
    KPI_PATIENTS          = "Patients"
    KPI_TOTAL_SCANS       = "Total Scans"
    KPI_ANALYSED          = "Analysed"
    KPI_PENDING           = "Pending"
    QA_UPLOAD_SCAN        = "Upload Scan"
    QA_VIEW_HISTORY       = "View History"
    QA_OPEN_RESULTS       = "Open Results"
    RECENT_ACTIVITY       = "Recent Activity"
    SYSTEM_STATUS         = "System Status"

    # Upload screen
    UPLOAD_TITLE          = "Upload Scan"
    DROP_ZONE_HINT        = "Tap to select a scan file"
    STEP_SELECT_FILE      = "Select File"
    STEP_VERIFY_INFO      = "Verify Info"
    STEP_UPLOAD           = "Upload"
    STEP_AI_ANALYSIS      = "AI Analysis"
    UPLOAD_SCAN_BTN       = "Upload Scan"
    RUN_SEGMENTATION_BTN  = "Run AI Segmentation"
    UPLOAD_ANOTHER_BTN    = "Upload Another"
    RUNNING_AI            = "Running AI segmentation\u2026"

    # Results screen
    RESULTS_TITLE         = "Results"
    PATIENT_INFO_SECTION  = "Patient Information"
    SEGMENTED_REGIONS     = "Segmented Regions"
    FULL_MANDIBLE_EXPORT  = "Full Mandible Export"
    DOWNLOAD_FULL_STL     = "Download Full STL"
    DOWNLOAD_FULL_DICOM   = "Download Full DICOM"
    NO_RESULTS_YET        = "No analysis results yet"
    ANALYSE_THIS_SCAN     = "Analyse This Scan"

    # Profile screen
    PERSONAL_INFO         = "Personal Information"
    SAVE_CHANGES_BTN      = "Save Changes"
    SIGN_OUT_BTN          = "Sign Out"
    SIGN_OUT_DIALOG_TITLE = "Sign Out"
    SIGN_OUT_CONFIRM      = "Sign Out"   # button text in Alert

    # Bottom navigation tabs
    TAB_HOME              = "Home"
    TAB_UPLOAD            = "Upload"
    TAB_HISTORY           = "History"
    TAB_RESULTS           = "Results"
    TAB_PROFILE           = "Profile"

    # Error messages (partial match)
    ERROR_EMPTY_FIELDS    = "Please enter your email and password."
    ERROR_ALL_REQUIRED    = "All fields are required."
    ERROR_INVALID_LOGIN   = "Invalid email or password."
    ERROR_SERVER          = "Cannot reach server"

    # Segmented region labels
    REGION_CHL            = "Condylar Head L"
    REGION_CHR            = "Condylar Head R"
    REGION_FULL           = "Full Mandible"


# ── Device info (for report) ───────────────────────────────────────────────────
DEVICE_NAME: str     = os.environ.get("ANDROID_DEVICE_NAME", "Android Emulator")
PLATFORM_VERSION: str = os.environ.get("ANDROID_PLATFORM_VERSION", "14")
APP_VERSION: str     = "1.0.0"    # from build.gradle versionName
APP_PACKAGE: str     = "com.dentaimobile"
