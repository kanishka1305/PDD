"""
AI Heavy User Scenario
======================
Simulates aggressive AI segmentation triggering to test inference limits.
Bypasses standard navigation and upload latency by repeatedly analyzing 
a pre-uploaded scan.
"""

from locust import HttpUser, task, between
from load_testing.config import LOAD_TEST_USERNAME, LOAD_TEST_PASSWORD, TEST_DATA_DIR

class AIHeavyUser(HttpUser):
    wait_time = between(2, 5)
    weight = 1  # Lower weight because this is an expensive operation

    def on_start(self):
        """Setup user session, authenticate, and prepare a scan ID."""
        self.token = None
        self.scan_id = None
        self.test_file_path = TEST_DATA_DIR / "synthetic_jaw.dcm"
        
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
        
        # Upload a scan once to be used repeatedly for AI analysis
        if self.token and self.test_file_path.exists():
            with open(self.test_file_path, "rb") as f:
                files = {"file": ("synthetic_jaw.dcm", f, "application/dicom")}
                upload_resp = self.client.post("/upload", headers=self._headers(), 
                                               files=files, name="POST /upload (Setup)")
                if upload_resp.status_code == 200:
                    self.scan_id = upload_resp.json().get("scan_id")

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task
    def trigger_segmentation(self):
        """Spam the AI Inference endpoint."""
        if not self.scan_id:
            return
            
        with self.client.post(f"/analyze/{self.scan_id}", headers=self._headers(),
                              name="POST /analyze/{scan_id}", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"AI Segment Failed: {resp.status_code}")
