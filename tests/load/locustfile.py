import os
from locust import HttpUser, task, between, events
import logging

class DentalAIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Called when a Locust start before any task is scheduled"""
        self.email = os.environ.get("TEST_USER_EMAIL", "")
        self.password = os.environ.get("TEST_USER_PASSWORD", "")
        self.token = None

        if self.email and self.password:
            response = self.client.post("/login", data={
                "email": self.email,
                "password": self.password
            }, catch_response=True)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.token = data.get("access_token")
                    response.success()
                else:
                    response.failure(f"Login failed: {data.get('message')}")
            else:
                response.failure(f"Login returned {response.status_code}")

    @task(3)
    def check_health(self):
        self.client.get("/health", name="/health")

    @task(2)
    def view_login_page(self):
        self.client.get("/login", name="/login")

    @task(2)
    def view_dashboard_page(self):
        # Even if unauthenticated, the page load itself can be tested (HTML delivery)
        self.client.get("/dashboard", name="/dashboard")

    @task(1)
    def get_scans(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/scans", headers=headers, name="/scans")
        else:
            # If no token, maybe test auth failure or just ignore
            with self.client.get("/scans", catch_response=True, name="/scans (unauth)") as response:
                if response.status_code in [401, 403]:
                    response.success()

    @task(1)
    def check_favicon(self):
        self.client.get("/favicon.ico", name="/favicon.ico")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logging.info("Starting load test...")
    if not environment.host:
        environment.host = os.environ.get("LOCUST_HOST", "http://127.0.0.1:8000")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logging.info("Load test completed.")
