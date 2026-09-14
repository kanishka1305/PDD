"""
Browser User Scenario
=====================
Simulates a clinician navigating the dashboard, fetching scan history, 
and viewing static assets without triggering heavy AI/Upload workflows.
"""

from locust import HttpUser, task, between
from load_testing.config import LOAD_TEST_USERNAME, LOAD_TEST_PASSWORD

class BrowserUser(HttpUser):
    wait_time = between(1, 4)
    weight = 5  # High frequency, simulating lots of dashboard reads

    def on_start(self):
        self.token = None
        # Login
        resp = self.client.post("/login", data={
            "email": LOAD_TEST_USERNAME,
            "password": LOAD_TEST_PASSWORD
        }, name="POST /login (Setup)")
        
        if resp.status_code == 200:
            try:
                if resp.json().get("success"):
                    self.token = resp.json().get("access_token")
            except Exception:
                pass

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def fetch_scans(self):
        """View history table."""
        self.client.get("/scans", headers=self._headers(), name="GET /scans")

    @task(2)
    def fetch_profile(self):
        """Dashboard stat refresh."""
        # Typically the UI fetches credentials or profile info
        self.client.post("/fetch_profile", headers=self._headers(), 
                         data={"id": "1"}, name="POST /fetch_profile")

    @task(4)
    def page_nav(self):
        """Navigate across frontend pages."""
        pages = ["/dashboard", "/history", "/viewer"]
        for p in pages:
            self.client.get(p, headers=self._headers(), name=f"GET {p}")

    @task(1)
    def health_check(self):
        """Ping API health check."""
        self.client.get("/health", name="GET /health")
