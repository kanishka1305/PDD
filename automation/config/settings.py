"""
DentAI Automation Framework — Central Configuration

All runtime values are read from environment variables first, then fall back
to sensible defaults. Never hardcode credentials or URLs in test files.

BASE_URL resolution order:
  1. BASE_URL environment variable (set by GitHub Actions)
  2. GITHUB_REPOSITORY env var → constructs the GitHub Pages URL automatically
  3. Hard fallback (update this to match your actual repo)
"""
import os
import pathlib

# ── Deployment Target ─────────────────────────────────────────────────────────
# In GitHub Actions the workflow sets:  BASE_URL: https://<owner>.github.io/<repo>
# Locally you can set BASE_URL in a .env file or shell environment.
# The GITHUB_REPOSITORY variable (format: "owner/repo") is set automatically
# by every GitHub Actions runner — we use it to construct the Pages URL when
# BASE_URL itself is not explicitly provided.

def _default_base_url() -> str:
    # Explicit override wins
    if os.environ.get("BASE_URL"):
        return os.environ["BASE_URL"].rstrip("/")
    # Auto-construct from GITHUB_REPOSITORY (works in any Actions runner)
    gh_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if gh_repo and "/" in gh_repo:
        owner, repo = gh_repo.split("/", 1)
        return f"https://{owner}.github.io/{repo}"
    # Local fallback — update to match your GitHub Pages URL
    return "https://skani.github.io/pdd_app"


BASE_URL = _default_base_url()

# ── Browser ───────────────────────────────────────────────────────────────────
BROWSER           = os.environ.get("BROWSER",       "chrome")
HEADLESS          = os.environ.get("HEADLESS",      "true").lower() == "true"
WINDOW_WIDTH      = int(os.environ.get("WINDOW_WIDTH",  "1920"))
WINDOW_HEIGHT     = int(os.environ.get("WINDOW_HEIGHT", "1080"))

# ── Timeouts (seconds) ────────────────────────────────────────────────────────
IMPLICIT_WAIT     = int(os.environ.get("IMPLICIT_WAIT",     "0"))
EXPLICIT_WAIT     = int(os.environ.get("EXPLICIT_WAIT",     "20"))
PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))

# ── Retry ─────────────────────────────────────────────────────────────────────
MAX_RETRIES  = int(os.environ.get("MAX_RETRIES",  "3"))
RETRY_DELAY  = float(os.environ.get("RETRY_DELAY", "2.0"))

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT_DIR       = pathlib.Path(__file__).parent.parent.parent
AUTO_DIR       = ROOT_DIR / "automation"
RESULTS_DIR    = ROOT_DIR / "Test Results"
SCREENSHOT_DIR = RESULTS_DIR / "Screenshots"
LOG_DIR        = RESULTS_DIR / "Logs"
JSON_DIR       = RESULTS_DIR / "JSON"
EXCEL_DIR      = RESULTS_DIR / "Excel"
HTML_DIR       = RESULTS_DIR / "HTML"
SUMMARY_DIR    = RESULTS_DIR / "Summary"
DATA_DIR       = AUTO_DIR   / "data"

# Create all output directories on import so pytest.ini log_file path exists
for _d in [SCREENSHOT_DIR, LOG_DIR, JSON_DIR, EXCEL_DIR, HTML_DIR, SUMMARY_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# ── Page URLs ─────────────────────────────────────────────────────────────────
PAGES = {
    "login":           f"{BASE_URL}/login.html",
    "signup":          f"{BASE_URL}/signup.html",
    "forgot_password": f"{BASE_URL}/forgot-password.html",
    "reset_password":  f"{BASE_URL}/reset-password.html",
    "dashboard":       f"{BASE_URL}/dashboard.html",
    "upload":          f"{BASE_URL}/upload.html",
    "results":         f"{BASE_URL}/results.html",
    "history":         f"{BASE_URL}/history.html",
    "viewer":          f"{BASE_URL}/viewer.html",
    "workflow":        f"{BASE_URL}/workflow.html",
    "refine":          f"{BASE_URL}/refine.html",
    "home":            f"{BASE_URL}/",
}

# ── Test credentials ──────────────────────────────────────────────────────────
VALID_EMAIL      = os.environ.get("TEST_EMAIL",      "doctor@dental-ai-test.com")
VALID_PASSWORD   = os.environ.get("TEST_PASSWORD",   "TestPass123!")
INVALID_EMAIL    = "notvalid@@@example"
INVALID_PASSWORD = "wrong"
ADMIN_EMAIL      = os.environ.get("ADMIN_EMAIL",     "admin@dental-ai-test.com")
ADMIN_PASSWORD   = os.environ.get("ADMIN_PASSWORD",  "AdminPass123!")
