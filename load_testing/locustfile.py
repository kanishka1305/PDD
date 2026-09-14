"""
Dental CBCT Application — Master Locustfile
===========================================
This is the main entry point for the load testing framework.
It imports the user scenarios and hooks up the Excel Reporter.
"""

import os
from locust import events
from load_testing.scenarios.workflow_user import WorkflowUser
from load_testing.scenarios.ai_heavy_user import AIHeavyUser
from load_testing.scenarios.browser_user import BrowserUser
from load_testing.utils.excel_reporter import ExcelReportGenerator
from load_testing.config import BASE_URL

# Expose classes so Locust finds them
__all__ = ["WorkflowUser", "AIHeavyUser", "BrowserUser"]

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Hook fired automatically when the load test finishes.
    Triggers the generation of the 13-sheet Excel Report.
    """
    if environment.stats.total.num_requests > 0:
        reporter = ExcelReportGenerator(environment)
        reporter.generate()
    else:
        print("\nNo requests made during load test. Skipping Excel Report generation.")

@events.init.add_listener
def on_init(environment, **kwargs):
    """
    Hook fired at startup. Good place to ensure test data exists.
    """
    from load_testing.test_data.generate_dicom import create_synthetic_dicom
    from load_testing.config import TEST_DATA_DIR
    
    TEST_DATA_DIR.mkdir(exist_ok=True)
    dcm_path = TEST_DATA_DIR / "synthetic_jaw.dcm"
    
    if not dcm_path.exists():
        create_synthetic_dicom(dcm_path)
