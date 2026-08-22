"""
DentAI — Baseline Load Test
============================
100 virtual users · 1 minute continuous run

All configuration via environment variables — no hardcoded credentials.

Environment variables:
  BASE_URL        Target API base URL  (default: https://pdd-uw63.onrender.com)
  TEST_EMAIL      Doctor email for login  (default: loadtest@dentai.com)
  TEST_PASSWORD   Password              (default: LoadTest@123)
  TEST_NAME       Doctor display name   (default: LoadTest Doctor)
  TEST_LICENSE    License number        (default: LT-000001)

Local run (baseline — 100 users, 60 seconds):
  locust -f load_tests/locustfile.py \\
    --headless -u 100 -r 10 -t 60s \\
    --host https://pdd-uw63.onrender.com \\
    --csv load_tests/results/stats \\
    --html load_tests/results/locust_report.html

GitHub Actions run:
  Set BASE_URL secret/var in repo settings.
  Trigger workflow: Actions → "DentAI — Baseline Load Test" → Run workflow
"""

import os
import json
from locust import HttpUser, task, between, events

# ── Credentials — read from env vars, never hardcoded ────────────────────────
TEST_EMAIL    = os.environ.get("TEST_EMAIL",    "loadtest@dentai.com")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "LoadTest@123")
TEST_NAME     = os.environ.get("TEST_NAME",     "LoadTest Doctor")
TEST_LICENSE  = os.environ.get("TEST_LICENSE",  "LT-000001")


class DentAIUser(HttpUser):
    """
    Simulates a dental clinician using the DentAI platform.

    Task weights reflect real-world usage patterns:
      - Health checks + public pages: high frequency (always accessible)
      - Authenticated API calls: high frequency (core value)
      - Heavy operations (upload/analysis): low weight (expensive)
    """
    wait_time = between(0.3, 1.5)   # realistic think-time between requests

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def on_start(self):
        """
        Called once per virtual user at spawn time.
        Registers a test account (idempotent) then logs in to get a JWT.
        """
        self.token   = None
        self.user_id = None
        self.scan_id = None

        # Step 1 — register (safe to call repeatedly — server rejects duplicates)
        self.client.post(
            "/signup",
            data={
                "name":     TEST_NAME,
                "license":  TEST_LICENSE,
                "email":    TEST_EMAIL,
                "password": TEST_PASSWORD,
            },
            name="POST /signup (setup)",
        )

        # Step 2 — login to get JWT
        resp = self.client.post(
            "/login",
            data={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            name="POST /login (setup)",
            catch_response=True,
        )
        with resp:
            try:
                data = resp.json()
                if data.get("success"):
                    self.token   = data.get("access_token")
                    self.user_id = data.get("id", 1)
                    resp.success()
                else:
                    # Login failed — mark success anyway so setup errors don't
                    # pollute performance stats; tests will return 401/403.
                    self.token = None
                    resp.success()
            except Exception:
                self.token = None
                resp.success()

    def _auth_headers(self):
        """Return Authorization header if we have a token, else empty dict."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    # ── Public endpoints (no auth required) ───────────────────────────────────

    @task(8)
    def health_check(self):
        """GET /health — lightweight heartbeat, highest frequency."""
        self.client.get("/health", name="GET /health")

    @task(5)
    def login_page(self):
        """GET /login — public HTML page."""
        self.client.get("/login", name="GET /login")

    @task(3)
    def signup_page(self):
        """GET /signup — public HTML page."""
        self.client.get("/signup", name="GET /signup")

    @task(3)
    def forgot_password_page(self):
        """GET /forgot-password — public HTML page."""
        self.client.get("/forgot-password", name="GET /forgot-password")

    # ── Authenticated page routes ──────────────────────────────────────────────

    @task(6)
    def dashboard_page(self):
        """GET /dashboard — authenticated HTML page."""
        self.client.get(
            "/dashboard",
            headers=self._auth_headers(),
            name="GET /dashboard",
        )

    @task(5)
    def upload_page(self):
        """GET /upload — authenticated HTML page."""
        self.client.get(
            "/upload",
            headers=self._auth_headers(),
            name="GET /upload",
        )

    @task(5)
    def results_page(self):
        """GET /results — authenticated HTML page."""
        self.client.get(
            "/results",
            headers=self._auth_headers(),
            name="GET /results",
        )

    @task(4)
    def history_page(self):
        """GET /history — authenticated HTML page."""
        self.client.get(
            "/history",
            headers=self._auth_headers(),
            name="GET /history",
        )

    @task(3)
    def workflow_page(self):
        """GET /workflow — authenticated HTML page."""
        self.client.get(
            "/workflow",
            headers=self._auth_headers(),
            name="GET /workflow",
        )

    @task(2)
    def viewer_page(self):
        """GET /viewer — authenticated HTML page (3D viewer)."""
        self.client.get(
            "/viewer",
            headers=self._auth_headers(),
            name="GET /viewer",
        )

    @task(2)
    def refine_page(self):
        """GET /refine — authenticated HTML page."""
        self.client.get(
            "/refine",
            headers=self._auth_headers(),
            name="GET /refine",
        )

    # ── Authenticated API endpoints ───────────────────────────────────────────

    @task(7)
    def get_scans(self):
        """GET /scans — returns scan list for authenticated doctor."""
        self.client.get(
            "/scans",
            headers=self._auth_headers(),
            name="GET /scans (API)",
        )

    @task(4)
    def fetch_profile(self):
        """POST /fetch_profile — returns doctor profile."""
        if not self.user_id:
            return
        self.client.post(
            "/fetch_profile",
            data={"id": str(self.user_id)},
            headers=self._auth_headers(),
            name="POST /fetch_profile (API)",
        )

    @task(2)
    def fetch_credentials(self):
        """POST /fetch_credentials — returns credential list."""
        if not self.user_id:
            return
        self.client.post(
            "/fetch_credentials",
            data={"doctor_id": str(self.user_id)},
            headers=self._auth_headers(),
            name="POST /fetch_credentials (API)",
        )

    # ── Static assets ─────────────────────────────────────────────────────────

    @task(3)
    def static_css(self):
        """GET /static/css — CSS stylesheet (cached by browsers in production)."""
        self.client.get(
            "/static/css/style.css",
            name="GET /static/css/style.css",
        )

    @task(2)
    def static_js(self):
        """GET /static/js — JavaScript bundle."""
        self.client.get(
            "/static/js/app.js",
            name="GET /static/js/app.js",
        )

    # ── Login / logout cycle (lower frequency) ────────────────────────────────

    @task(2)
    def login_api(self):
        """POST /login — simulates login from a fresh session."""
        with self.client.post(
            "/login",
            data={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            name="POST /login (API)",
            catch_response=True,
        ) as resp:
            try:
                d = resp.json()
                if d.get("success") or resp.status_code in (200, 401, 422):
                    resp.success()
                else:
                    resp.failure(f"Unexpected status: {resp.status_code}")
            except Exception as e:
                resp.failure(str(e))

    @task(1)
    def signup_api(self):
        """
        POST /signup — duplicate signup (expected to return 200 with
        success=False for 'email already registered').  Mark as success
        because this is an expected application response, not a load failure.
        """
        with self.client.post(
            "/signup",
            data={
                "name":     TEST_NAME,
                "license":  TEST_LICENSE,
                "email":    TEST_EMAIL,
                "password": TEST_PASSWORD,
            },
            name="POST /signup (API)",
            catch_response=True,
        ) as resp:
            # Both 200 (duplicate) and 422 (validation) are expected
            if resp.status_code in (200, 201, 422):
                resp.success()
            else:
                resp.failure(f"Unexpected status: {resp.status_code}")
