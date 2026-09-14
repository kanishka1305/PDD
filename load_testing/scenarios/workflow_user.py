"""
Full Workflow User Scenario
===========================
Simulates a complete user journey:
Login -> Dashboard -> Upload DICOM -> Analyze -> Export STL -> Export DICOM
"""

import os
from locust import HttpUser, task, between
from load_testing.config import TEST_DATA_DIR, LOAD_TEST_USERNAME, LOAD_TEST_PASSWORD

class WorkflowUser(HttpUser):
    wait_time = between(1, 3)
    weight = 3  # Medium frequency compared to browser users

    def on_start(self):
        """Setup user session and authenticate."""
        self.token = None
        self.scan_id = None
        self.test_file_path = TEST_DATA_DIR / "synthetic_jaw.dcm"
        
        # Ensure user exists (idempotent signup)
        self.client.post("/signup", data={
            "name": "E2E Load User",
            "license": "LT-E2E-001",
            "email": LOAD_TEST_USERNAME,
            "password": LOAD_TEST_PASSWORD
        }, name="POST /signup (Setup)")
        
        # Login
        with self.client.post("/login", data={
            "email": LOAD_TEST_USERNAME,
            "password": LOAD_TEST_PASSWORD
        }, name="POST /login", catch_response=True) as resp:
            try:
                if resp.status_code == 200 and resp.json().get("success"):
                    self.token = resp.json().get("access_token")
                    resp.success()
                else:
                    resp.failure("Login failed")
            except Exception:
                resp.failure("Login response was not JSON")
                
    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task
    def full_clinical_workflow(self):
        """Executes the primary heavy workflow."""
        if not self.token:
            return

        # 1. Dashboard Load
        self.client.get("/dashboard", headers=self._headers(), name="GET /dashboard")
        self.client.get("/scans", headers=self._headers(), name="GET /scans")
        
        # 2. Upload CBCT/DICOM
        if not self.test_file_path.exists():
            return  # skip if test data missing

        with open(self.test_file_path, "rb") as f:
            files = {"file": ("synthetic_jaw.dcm", f, "application/dicom")}
            with self.client.post("/upload", headers=self._headers(), files=files, 
                                  name="POST /upload", catch_response=True) as resp:
                if resp.status_code == 200:
                    data = resp.json()
                    self.scan_id = data.get("scan_id")
                    resp.success()
                else:
                    resp.failure(f"Upload failed: {resp.status_code}")
                    return

        if not self.scan_id:
            return
            
        # 3. AI Segmentation (Inference)
        with self.client.post(f"/analyze/{self.scan_id}", headers=self._headers(),
                              name="POST /analyze/{scan_id}", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Analysis failed: {resp.status_code}")
                return

        # 4. View Results
        self.client.get("/results", headers=self._headers(), name="GET /results")

        # 5. Export STL (Full mandible)
        with self.client.get(f"/stl-region/{self.scan_id}/full", headers=self._headers(),
                             name="GET /stl-region/{scan_id}/{region}", catch_response=True) as resp:
            if resp.status_code in [200, 404]: # 404 is fine if synthetic data has no bone
                resp.success()
            else:
                resp.failure(f"STL Export failed: {resp.status_code}")

        # 6. Export DICOM (Condyle region)
        with self.client.get(f"/export-dicom/{self.scan_id}/condylar_head_L", headers=self._headers(),
                             name="GET /export-dicom/{scan_id}/{region}", catch_response=True) as resp:
            if resp.status_code in [200, 404]:
                resp.success()
            else:
                resp.failure(f"DICOM Export failed: {resp.status_code}")
