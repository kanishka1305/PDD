"""
Test Data Management — all test data in one place.
"""
import os

# ── Credentials ───────────────────────────────────────────────────────────────
VALID_USER = {
    "name":     "Dr. Test Doctor",
    "license":  "LIC-TEST-001",
    "email":    os.environ.get("TEST_EMAIL", "doctor@dental-ai-test.com"),
    "password": os.environ.get("TEST_PASSWORD", "TestPass123!"),
}

INVALID_USERS = [
    {"email": "",                    "password": "",             "label": "empty_both"},
    {"email": "notanemail",          "password": "Test123!",     "label": "bad_email_format"},
    {"email": "x@x",                 "password": "Test123!",     "label": "incomplete_email"},
    {"email": VALID_USER["email"],   "password": "wrongpass",    "label": "wrong_password"},
    {"email": "nobody@nowhere.com",  "password": "Test123!",     "label": "unknown_email"},
    {"email": "' OR '1'='1",         "password": "x",            "label": "sqli_email"},
    {"email": "<script>alert(1)</script>@x.com", "password": "x","label": "xss_email"},
    {"email": "a" * 300 + "@x.com",  "password": "Test123!",     "label": "overlong_email"},
    {"email": VALID_USER["email"],   "password": "a",            "label": "too_short_password"},
    {"email": VALID_USER["email"],   "password": "a" * 200,      "label": "overlong_password"},
]

SIGNUP_VALID = {
    "name":     "Dr. Automation Test",
    "license":  "LIC-AUTO-999",
    "email":    "autotest@dental-ai-test.com",
    "password": "AutoTest123!",
}

SIGNUP_INVALID = [
    {"name": "",              "license": "LIC001", "email": "x@x.com",  "password": "Test123!", "label": "empty_name"},
    {"name": "Dr X",         "license": "",        "email": "x@x.com",  "password": "Test123!", "label": "empty_license"},
    {"name": "Dr X",         "license": "LIC001",  "email": "",          "password": "Test123!", "label": "empty_email"},
    {"name": "Dr X",         "license": "LIC001",  "email": "x@x.com",  "password": "",         "label": "empty_password"},
    {"name": "Dr X",         "license": "LIC001",  "email": "bademail", "password": "Test123!", "label": "invalid_email"},
    {"name": "Dr X",         "license": "LIC001",  "email": "x@x.com",  "password": "123",      "label": "weak_password"},
    {"name": "A" * 300,      "license": "LIC001",  "email": "x@x.com",  "password": "Test123!", "label": "overlong_name"},
]

FORGOT_PASSWORD_DATA = [
    {"email": VALID_USER["email"],  "label": "valid_email"},
    {"email": "nobody@x.com",       "label": "unknown_email"},
    {"email": "",                   "label": "empty_email"},
    {"email": "notanemail",         "label": "invalid_format"},
]

# ── Navigation ────────────────────────────────────────────────────────────────
ALL_PAGES = [
    "login", "signup", "forgot_password", "dashboard",
    "upload", "results", "history", "viewer", "workflow", "refine",
]

# ── UI Validation ─────────────────────────────────────────────────────────────
EXPECTED_PAGE_TITLES = {
    "login":           "DentAI",
    "signup":          "DentAI",
    "forgot_password": "DentAI",
    "dashboard":       "DentAI",
    "upload":          "DentAI",
    "results":         "DentAI",
    "history":         "DentAI",
    "viewer":          "DentAI",
    "workflow":        "DentAI",
    "refine":          "DentAI",
}

EXPECTED_LOGIN_ELEMENTS = [
    "email", "password", "login-btn", "signup-link",
]

EXPECTED_SIGNUP_ELEMENTS = [
    "name", "license", "email", "password", "signup-btn", "login-link",
]

# ── Viewport sizes for responsive tests ───────────────────────────────────────
VIEWPORTS = {
    "mobile_s":  (320,  568),
    "mobile_l":  (414,  896),
    "tablet":    (768, 1024),
    "laptop":    (1280, 800),
    "desktop":   (1920,1080),
    "4k":        (2560,1440),
}

# ── Injection payloads ────────────────────────────────────────────────────────
SQL_PAYLOADS = [
    "' OR '1'='1",
    "admin'--",
    "' UNION SELECT 1,2,3--",
    "'; DROP TABLE doctors;--",
    "1' AND SLEEP(5)--",
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "'><svg onload=alert(1)>",
]

BOUNDARY_VALUES = {
    "name_min":       "AB",
    "name_max":       "A" * 100,
    "name_over":      "A" * 101,
    "password_min":   "Pass123!",
    "password_short": "Pas1!",
    "email_valid":    "test@example.com",
    "email_unicode":  "tëst@example.com",
}
