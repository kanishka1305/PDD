"""
Load Testing Configuration & Thresholds
========================================
Reads environment variables for base URL and credentials.
Defines pass/fail thresholds for the Excel report generation.
"""

import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
TEST_DATA_DIR = BASE_DIR / "test_data"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# ── Targets & Credentials ─────────────────────────────────────────────────────
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

# For testing, we use multiple concurrent virtual users.
# The scenario scripts will register these credentials on-the-fly.
LOAD_TEST_USERNAME = os.environ.get("LOAD_TEST_USERNAME", "loadtest_user@dentai.com")
LOAD_TEST_PASSWORD = os.environ.get("LOAD_TEST_PASSWORD", "LoadTest@123")

# ── Performance Thresholds ────────────────────────────────────────────────────
# Used by the Excel reporter to determine PASS/FAIL status automatically.

THRESHOLDS = {
    # General API constraints
    "global_error_rate_percent": 1.0,    # Max 1% error rate allowed
    "global_p95_response_ms":    2000.0, # Max 2 seconds for P95 across all APIs
    "global_p99_response_ms":    5000.0, # Max 5 seconds for P99 across all APIs
    
    # Specific workflows
    "upload_p95_ms":             3000.0, # Target 3 seconds for file upload
    "analyze_p95_ms":            8000.0, # AI Segmentation target latency (mocked/cached usually fast, actual AI inference might be slow, adjust based on actual model baseline)
    "export_p95_ms":             2500.0, # STL / DICOM generation
}
