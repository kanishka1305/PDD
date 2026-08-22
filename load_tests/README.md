# DentAI — Baseline Load Test

> **Tool**: [Locust](https://locust.io/) · **Target**: DentAI CBCT AI Platform API  
> **Config**: 100 virtual users · 1-minute continuous run

---

## Quick Start (Local)

### 1. Install dependencies

```bash
pip install -r requirements-test.txt
```

Or install just the load-testing dependencies:

```bash
pip install locust==2.32.3 openpyxl==3.1.5 requests==2.32.3
```

### 2. Run the baseline test

```bash
locust -f load_tests/locustfile.py \
  --headless \
  -u 100 \
  -r 10 \
  -t 60s \
  --host https://pdd-uw63.onrender.com \
  --csv load_tests/results/stats \
  --html load_tests/results/locust_report.html
```

### 3. Generate Excel + HTML reports

```bash
python load_test/generate_load_report.py
```

Reports are written to:
- `reports/baseline_load_test_report.xlsx`
- `reports/baseline_load_test_report.html`

---

## Configuration

All settings are controlled through **environment variables** — no hardcoded values.

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://pdd-uw63.onrender.com` | Target API base URL |
| `TEST_EMAIL` | `loadtest@dentai.com` | Test account email |
| `TEST_PASSWORD` | `LoadTest@123` | Test account password |
| `TEST_NAME` | `LoadTest Doctor` | Display name for test account |
| `TEST_LICENSE` | `LT-000001` | License number for test account |
| `USERS` | `100` | Number of virtual users |
| `SPAWN_RATE` | `10` | Users spawned per second |
| `DURATION` | `60s` | Test duration |

### Performance Thresholds

| Variable | Default | Meaning |
|---|---|---|
| `THRESH_ERROR_RATE` | `1.0` | Maximum error rate (%) |
| `THRESH_AVG_RT` | `500` | Maximum average response time (ms) |
| `THRESH_P95` | `1000` | Maximum P95 response time (ms) |
| `THRESH_P99` | `2000` | Maximum P99 response time (ms) |

---

## Running Against a Custom URL

```bash
BASE_URL=https://my-api.example.com \
  locust -f load_tests/locustfile.py \
  --headless -u 100 -r 10 -t 60s \
  --host https://my-api.example.com \
  --csv load_tests/results/stats \
  --html load_tests/results/locust_report.html
```

## Running With Custom Credentials

```bash
TEST_EMAIL=myemail@example.com \
TEST_PASSWORD=mysecretpassword \
  locust -f load_tests/locustfile.py \
  --headless -u 100 -r 10 -t 60s \
  --host https://pdd-uw63.onrender.com \
  --csv load_tests/results/stats \
  --html load_tests/results/locust_report.html
```

## Running With Custom Thresholds

```bash
THRESH_ERROR_RATE=0.5 \
THRESH_AVG_RT=300 \
THRESH_P95=800 \
THRESH_P99=1500 \
  python load_test/generate_load_report.py
```

---

## GitHub Actions

### Manual Trigger

1. Go to **Actions** tab in your GitHub repository
2. Select **"DentAI — Baseline Load Test"** workflow
3. Click **"Run workflow"**
4. Optionally override: `base_url`, `users`, `duration`, `spawn_rate`
5. Click **"Run workflow"**

### Automatic Schedule

The workflow runs automatically:
- **Every Monday at 06:00 UTC** (weekly baseline)
- On every push to `main` or `master`

### Artifacts

After the workflow completes, download the `baseline-load-test-report` artifact from the **Artifacts** section at the bottom of the workflow run page. It contains:

| File | Description |
|---|---|
| `baseline_load_test_report.xlsx` | 4-sheet Excel report (Summary, Endpoint Stats, HTTP Codes, Performance Summary) |
| `baseline_load_test_report.html` | Full HTML report with KPI cards and tables |
| `stats_stats.csv` | Raw per-endpoint Locust statistics |
| `stats_stats_history.csv` | Time-series RPS and response time data |
| `stats_failures.csv` | List of failed requests |
| `stats_exceptions.csv` | Python exceptions during the test |
| `locust_report.html` | Locust's built-in interactive HTML report |

---

## Endpoints Tested

| Endpoint | Method | Type | Auth Required |
|---|---|---|---|
| `/health` | GET | Health check | No |
| `/login` | GET | Public page | No |
| `/signup` | GET | Public page | No |
| `/forgot-password` | GET | Public page | No |
| `/dashboard` | GET | App page | Yes |
| `/upload` | GET | App page | Yes |
| `/results` | GET | App page | Yes |
| `/history` | GET | App page | Yes |
| `/workflow` | GET | App page | Yes |
| `/viewer` | GET | App page | Yes |
| `/refine` | GET | App page | Yes |
| `/scans` | GET | API | Yes |
| `/fetch_profile` | POST | API | Yes |
| `/fetch_credentials` | POST | API | Yes |
| `/static/css/style.css` | GET | Static asset | No |
| `/static/js/app.js` | GET | Static asset | No |
| `/login` | POST | Auth API | No |
| `/signup` | POST | Auth API | No |

---

## Report Sheets (Excel)

| Sheet | Contents |
|---|---|
| **Summary** | Test configuration, aggregated metrics, overall PASS/FAIL |
| **Endpoint Statistics** | Per-endpoint requests, failures, response times (min/avg/max/P90/P95/P99) |
| **HTTP Status Codes** | Distribution of 200/401/422/429/500/503 responses |
| **Performance Summary** | Threshold evaluation table with PASS/FAIL per metric |

---

## Notes

- **Duplicate signups**: The test re-uses the same email for all 100 virtual users. Duplicate signup responses (HTTP 200 with `success=False`) are treated as expected and counted as success, not failure.
- **Unauthenticated 401s**: If the JWT token cannot be obtained, protected endpoints return 401. This is tracked as an expected application response, not a load-test failure.
- **No data pollution**: The test uses a dedicated `loadtest@dentai.com` account. Keep this account in your test/staging environment only.
