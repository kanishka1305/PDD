# Load Testing System

This directory contains the automated baseline and load testing system for the application, built with [Locust](https://locust.io/) and Python `openpyxl`.

## Requirements

Install the dependencies:
```bash
pip install -r ../../requirements-load-testing.txt
```

## Setup and Configuration

The test can be configured through environment variables:

- `LOCUST_HOST`: The base URL of the target application (e.g., `http://127.0.0.1:8000`).
- `TEST_USER_EMAIL`: (Optional) Email address for authentication during the test.
- `TEST_USER_PASSWORD`: (Optional) Password for authentication.

### Acceptance Criteria Thresholds

The Excel report generator uses these configurable thresholds to determine if the test passes or fails. The defaults are:

- `EXPECTED_USERS`: 100
- `EXPECTED_DURATION`: 60 (seconds)
- `MAX_FAILURE_RATE`: 1.0 (%)
- `MAX_AVG_RT`: 500.0 (ms)
- `MAX_P95_RT`: 1000.0 (ms)
- `MAX_MAX_RT`: 3000.0 (ms)

## Local Execution

To run the test locally:

1. Start your backend application.
2. Run the Locust test in headless mode for 1 minute:
   ```bash
   locust -f tests/load/locustfile.py --headless -u 100 -r 10 --run-time 1m --csv=reports/load_testing/locust_stats
   ```
3. Generate the Excel report:
   ```bash
   python tests/load/test_report_generator.py --csv-prefix reports/load_testing/locust_stats --output reports/load_testing/load_test_report.xlsx
   ```

## GitHub Actions Execution

The load tests are fully integrated into GitHub Actions via the `.github/workflows/load-testing.yml` workflow.

To run from GitHub Actions:
1. Go to the **Actions** tab in your repository.
2. Select **Load Testing** from the left sidebar.
3. Click **Run workflow**.
4. You can optionally override the target URL, virtual users, spawn rate, and duration.
5. If testing a secure environment, ensure the `TEST_USER_EMAIL` and `TEST_USER_PASSWORD` secrets are set in your GitHub repository settings.

## Report Access

After a GitHub Actions run (whether it passes or fails), the Excel report and raw CSV files are uploaded as artifacts.

To download the report:
1. Go to the summary page of the workflow run.
2. Scroll down to the **Artifacts** section.
3. Download the `load-testing-report-<commit-sha>` zip file.
4. Extract it to view `load_test_report.xlsx`.

## Report Generation Validation

To validate that the report generator works correctly:
```bash
python -m unittest tests/load/test_report_validation.py
```
