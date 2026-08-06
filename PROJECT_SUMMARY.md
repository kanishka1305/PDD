# DentAI — Project Training Summary
> Use this document to train ChatGPT (or any AI assistant) about the DentAI platform.
> It covers every component: purpose, architecture, tech stack, APIs, database, security, testing, and CI/CD.

---

## 1. What Is DentAI?

DentAI is a full-stack AI-powered dental imaging platform built for oral surgeons and dentists. It allows medical professionals to:

- Upload CBCT (Cone Beam CT) dental scans in DICOM, NIfTI, or ZIP format
- Automatically segment the mandible (jaw bone) using AI algorithms
- View a 3D interactive model of the segmented jaw divided into 9 anatomical regions
- Download STL files (for surgical planning / 3D printing) and DICOM exports per region
- Manage their patient scan history, profile, and professional credentials
- Access everything from a web browser, a React Native mobile app, or a native Android app

The system is used by dental professionals (doctors) who log in with a licensed account.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Web Frontend     │  │ React Native App │  │ Android APK  │  │
│  │ (React 18 + Vite)│  │ (DentAI-Mobile)  │  │ (Kotlin)     │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘  │
└───────────┼─────────────────────┼────────────────────┼──────────┘
            │           REST API (HTTP + JWT Bearer token)
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND LAYER                             │
│                 FastAPI (Python 3.11)                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │  Auth    │ │  Upload  │ │ Analysis │ │  STL / Export    │   │
│  │  Router  │ │  Router  │ │  Router  │ │  Routers         │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              AI / Medical Imaging Services               │   │
│  │  load volume → normalise → segment → 9-region partition  │   │
│  │  → STL export → DICOM export → JSON report               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                │
│  MySQL database: dental_ai                                      │
│  Tables: doctors, scans, credentials, reset_tokens             │
│  File storage: /uploads (DICOM, NIfTI, ZIP)                    │
│  File output:  /results (PNG previews, STL, JSON reports)      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Tech Stack

### Backend
| Component | Technology |
|-----------|------------|
| Framework | FastAPI (Python 3.11) |
| Database | MySQL (mysql-connector-python) |
| Auth | JWT (python-jose) + bcrypt password hashing |
| Medical Imaging | pydicom, nibabel, numpy |
| AI / Segmentation | NumPy threshold + anatomical partitioning |
| 3D Export | numpy-stl (STL files), pydicom (DICOM export) |
| Visualisation | matplotlib (segmentation preview PNG) |
| Rate Limiting | slowapi |
| File Validation | python-magic (MIME type inspection) |
| ASGI Server | Uvicorn |

### Web Frontend (dental-ai-frontend/)
| Component | Technology |
|-----------|------------|
| Framework | React 18 + TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| 3D Viewer | Three.js |
| Routing | React Router v6 |
| HTTP Client | Axios |

### Mobile App (DentAI-Mobile/)
| Component | Technology |
|-----------|------------|
| Framework | React Native 0.76.5 |
| Language | TypeScript |
| Navigation | React Navigation (Stack) |
| HTTP Client | Axios + AsyncStorage (token storage) |
| Platform | Android (+ iOS compatible) |

### Static HTML Frontend (served by FastAPI)
- Plain HTML5 + CSS + vanilla JavaScript
- Served directly from `app/static/`
- Used for GitHub Pages deployment

### Android Native App (Dental-segment-frontend/)
- Kotlin / Gradle
- Compiled to `.apk`

### Automation / Testing
| Component | Technology |
|-----------|------------|
| E2E Tests | Python + Selenium WebDriver |
| Test Runner | pytest + pytest-html + pytest-xdist |
| Framework Pattern | Page Object Model (POM) |
| JS Tests | Node.js + Selenium-webdriver + Mocha |
| Load Testing | Locust (100 VUs, 1 minute) |
| Reports | openpyxl (Excel) + HTML |

### CI/CD
| Component | Technology |
|-----------|------------|
| Platform | GitHub Actions |
| Deployment | GitHub Pages |
| SAST | Bandit + Semgrep |
| Secret Scanning | Gitleaks |
| Dependency CVEs | Safety + Trivy |
| Test Reports | Excel (.xlsx) + HTML artifacts |

---

## 4. Database Schema

Database name: `dental_ai`

### doctors
```sql
id            INT AUTO_INCREMENT PRIMARY KEY
name          VARCHAR(255) NOT NULL
license       VARCHAR(255)          -- dental license number
email         VARCHAR(255) UNIQUE NOT NULL
password      VARCHAR(255) NOT NULL  -- bcrypt hash
phone         VARCHAR(50)
clinic        VARCHAR(255)
created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### scans
```sql
id            INT AUTO_INCREMENT PRIMARY KEY
patient_name  VARCHAR(255)
patient_id    VARCHAR(255)
filename      VARCHAR(255)
filepath      VARCHAR(500)
modality      VARCHAR(100)          -- DICOM, NIfTI, ZIP
status        VARCHAR(50)           -- pending, completed
doctor_id     INT                   -- foreign key → doctors.id
created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### credentials
```sql
id                INT AUTO_INCREMENT PRIMARY KEY
doctor_id         INT NOT NULL REFERENCES doctors(id)
credential_type   VARCHAR(100)      -- e.g. "Board Certification"
credential_number VARCHAR(255)
issue_date        VARCHAR(50)
expiry_date       VARCHAR(50)
```

### reset_tokens
```sql
token       VARCHAR(128) PRIMARY KEY  -- cryptographically random
email       VARCHAR(255)
expires_at  DATETIME                  -- 15-minute TTL
used        TINYINT(1) DEFAULT 0      -- single-use enforcement
```

---

## 5. Backend API Endpoints

All endpoints are on the FastAPI backend (default: `http://localhost:8000`).

### Authentication & Profile
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/login` | No | Login with email + password → returns JWT |
| POST | `/signup` | No | Register new doctor account |
| POST | `/forgot-password` | No | Request password reset email |
| POST | `/reset-password` | No | Reset password using token |
| POST | `/fetch_profile` | Yes | Get doctor profile (IDOR-safe) |
| POST | `/update_profile` | Yes | Update name, email, phone, clinic |
| POST | `/change_password` | Yes | Change password |
| POST | `/add_credential` | Yes | Add professional credential |
| POST | `/fetch_credentials` | Yes | List credentials for a doctor |

### Scan Management
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/scans` | Yes | List all scans for authenticated doctor |
| POST | `/upload` | Yes | Upload DICOM/NIfTI/ZIP scan file |
| POST | `/analyze/{scan_id}` | Yes | Run AI analysis on a scan |

### Results & Export
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/results-img` | Yes | Serve segmentation preview PNG |
| GET | `/stl/{scan_id}` | Yes | Download full mandible STL |
| GET | `/stl-region/{scan_id}/{region}` | Yes | Download STL for one region |
| GET | `/export-dicom/{scan_id}/{region}` | Yes | Export DICOM for one region |

### Pages (HTML)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirects to `/login` |
| GET | `/login` | Login page |
| GET | `/signup` | Signup page |
| GET | `/forgot-password` | Forgot password page |
| GET | `/reset-password` | Reset password page |
| GET | `/dashboard` | Dashboard page |
| GET | `/upload` | Upload page |
| GET | `/results` | Results viewer page |
| GET | `/history` | Scan history page |
| GET | `/workflow` | Workflow guide page |
| GET | `/viewer` | 3D STL viewer page |
| GET | `/refine` | Refine segmentation page |

### Utility
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check → returns `{"status": "ok"}` |

---

## 6. AI / Segmentation Pipeline

When `POST /analyze/{scan_id}` is called, this pipeline runs:

```
1. Load Volume
   ├── Single DICOM (.dcm) → pixel_array → (1, rows, cols)
   ├── DICOM folder        → stack sorted slices → (N, rows, cols)
   └── NIfTI (.nii/.gz)   → nibabel load → moveaxis → (slices, rows, cols)

2. Normalise
   └── Min-max normalise to [0, 1] float32

3. Segment (threshold)
   └── Binary threshold at 0.5 (falls back to 0.4→0.3→0.2→0.1→0.05)
       → Returns uint8 mask same shape as volume

4. Partition into 9 Anatomical Regions
   ├── 3D volume (z_range ≥ 2): partitioned by Z slices
   │   ├── Superior 25%  → condylar_head_L, condylar_head_R, coronoid_L, coronoid_R
   │   ├── Mid 25-55%    → angle_ramus_L, angle_ramus_R
   │   └── Inferior 45%  → body_L, body_R, symphyseal_parasymphyseal
   └── 2D / single-slice: partitioned by Y rows (same zones)

5. Calculate Metrics
   ├── Total voxel count
   ├── Estimated volume per region (mm³)
   ├── Cortical bone: 65% of total volume
   └── Trabecular bone: 35% of total volume

6. Export
   ├── Segmentation preview PNG (matplotlib)
   ├── STL file — full mandible
   ├── STL file — per region (9 files)
   └── DICOM export — per region

7. Generate JSON Report
   └── Saved to results/{scan_id}_report.json
       Contains: volumes, regions, nerve distance, bone loss %, confidence, report_id
```

---

## 7. Frontend Pages

### Web App (React SPA + Static HTML)
| Page | Route | Purpose |
|------|-------|---------|
| Login | `/login` | Email + password authentication |
| Signup | `/signup` | Doctor registration (name, license, email, password) |
| Forgot Password | `/forgot-password` | Request reset email |
| Reset Password | `/reset-password` | Enter new password with token |
| Dashboard | `/dashboard` | Overview of recent scans and metrics |
| Upload | `/upload` | Drag-and-drop DICOM/NIfTI/ZIP upload |
| Results | `/results` | View segmentation output, metrics, 3D model |
| History | `/history` | Browse past scans with search/filter |
| Workflow | `/workflow` | Step-by-step guide for using the platform |
| Viewer | `/viewer` | Interactive Three.js 3D STL viewer |
| Refine | `/refine` | Adjust segmentation parameters |

### Mobile App Screens
Same pages as above adapted for mobile with React Native navigation stack.

---

## 8. Security Measures Implemented

The codebase has explicit security fixes labelled by issue ID (SEC-001 through SEC-022):

| ID | Issue | Fix Applied |
|----|-------|-------------|
| SEC-001 | Hardcoded credentials | Removed — env vars used |
| SEC-002 | Unauthenticated endpoints | JWT `require_auth` dependency on all data routes |
| SEC-003 | CORS wildcard (`*`) | Restricted to explicit allowed origins list |
| SEC-004 | IDOR (access other users' data) | Ownership check: `caller_id != requested_id → 403` |
| SEC-005 | Path traversal in filename | `basename()` + regex allowlist + resolved path check |
| SEC-006 | Zip Slip | All zip entries validated before extraction |
| SEC-007 | Reset token in API response | Token stored in DB only, never returned in response |
| SEC-008 | SHA-256 password hashing | Replaced with bcrypt (cost=12) |
| SEC-009 | Path traversal in `/results-img` | Path resolved + confined to `results/` directory |
| SEC-010 | No input validation | Pydantic models with field constraints |
| SEC-011 | Raw exceptions returned | Generic 500 responses, errors logged server-side only |
| SEC-012 | No rate limiting | slowapi: 5 login attempts/minute/IP |
| SEC-013 | MIME type not checked | python-magic inspects file bytes, not just extension |
| SEC-014 | `/volume-test` exposed in production | Returns 404 in production (DEBUG_MODE=false) |
| SEC-015 | No file size limit | 100 MB maximum enforced at header + content level |
| SEC-016 | Missing security headers | X-Frame-Options, CSP, HSTS, X-Content-Type-Options, etc. |
| SEC-017 | Reset tokens stored insecurely | DB table with 15-min TTL + single-use enforcement |
| SEC-018 | `/scans` returned all doctors' data | Filtered by `doctor_id` from JWT |
| SEC-019 | Swagger/OpenAPI exposed in production | Disabled when `DEBUG_MODE != true` |
| SEC-022 | Static pages exposed data | HTML pages serve no data — auth enforced by API layer |

---

## 9. Automation Test Suite

Located in `automation/` — Python + Selenium + pytest with Page Object Model.

### Test Modules
| Module | Test Count | Coverage Area |
|--------|-----------|---------------|
| test_authentication.py | 40 | Login, signup, logout, password reset, token handling |
| test_forms.py | 90 | All form inputs — valid/invalid/boundary values |
| test_navigation.py | 30 | Page routing, redirects, menu navigation |
| test_ui_validation.py | 50 | Field validation messages, error states, UI state |
| test_regression.py | 170 | Full regression — auth, CRUD, security, accessibility, performance, IDOR |
| **Total** | **380+** | **Complete platform coverage** |

### Simulated Test Catalog (generate_automation_report.py)
Used for demo/report generation with realistic pass rates:
| Category | Tests | Pass Rate |
|----------|-------|-----------|
| test_authentication | 40 | 80% |
| test_authorization | 40 | 75% |
| test_navigation | 30 | 93% |
| test_ui_validation | 50 | 86% |
| test_forms | 50 | 82% |
| test_forms_input | 40 | 78% |
| test_session | 20 | 85% |
| test_file_upload | 20 | 80% |
| test_accessibility | 20 | 90% |
| test_responsive | 20 | 95% |
| test_performance | 20 | 70% |
| test_regression | 50 | 88% |

### Report Output
Each test run produces:
- `Automation_Test_Report.xlsx` — 6 sheets: All Tests, Passed, Failed, Skipped, Metrics, Defects
- `Passed_Test_Cases.xlsx`
- `Failed_Test_Cases.xlsx`
- `Summary_Report.xlsx` — pass rate per module
- `execution-report.html` — self-contained HTML report
- Screenshots of all failures
- JSON results file for pipeline processing

---

## 10. CI/CD Pipeline (GitHub Actions)

### Workflow: deploy-and-test.yml
Triggers on push to `main`, `master`, `develop`, and PRs.

```
Job 1: build-and-analyze
  → Checkout + install Python deps
  → Validate HTML static files
  → Run Bandit SAST
  → Run Semgrep SAST
  → Upload: static-analysis-reports artifact

Job 2: deploy (needs: build-and-analyze)
  → Copy static HTML to _site/
  → Deploy to GitHub Pages
  → Output: page_url

Job 3: verify-deployment (needs: deploy)
  → Wait 30 seconds for propagation
  → Poll URL up to 10 times (15s intervals)
  → Output: verified=true/false, live_url

Job 4: e2e-tests (needs: verify-deployment, only if verified=true)
  → Install Selenium + Chrome
  → Run full pytest suite against live site
  → Upload: test-json-results artifact (1 day)

Job 5: generate-excel-report (needs: build-and-analyze + e2e-tests, if: always())
  → Downloads JSON results (continue-on-error: true)
  → Generates all 4 Excel workbooks
  → Upload: excel-reports-{run_number} artifact (90 days)  ← PRIMARY DOWNLOAD
  → Upload: e2e-test-results-{run_number} artifact (30 days)
  → Publishes summary to GitHub Step Summary

Job 6: store-history (needs: generate-excel-report)
  → Logs run number + commit + date to history.log
  → Upload: execution-history artifact
```

**Important:** `generate-excel-report` uses `if: always()` so Excel reports are generated on every run, even if the live site was not reachable and e2e-tests were skipped.

### Workflow: security-review.yml
Triggers on push/PR + weekly schedule (Mondays 02:00 UTC).

Tools run:
- **Bandit** — Python SAST (HIGH/CRITICAL findings fail the pipeline)
- **Semgrep** — OWASP Top 10 + injection rules
- **Safety** — Python dependency CVE scan
- **Gitleaks** — Secret/credential scanning in git history
- **Trivy** — Filesystem vulnerability scan (CRITICAL + HIGH severity)
- **Dependency Review** — On PRs only (GitHub native)

---

## 11. File / Folder Structure

```
pdd_app/
├── Dental (1)/Dental/app/         ← FastAPI Backend
│   ├── main.py                    ← App entry, routes, middleware
│   ├── api/
│   │   ├── auth.py                ← Login, signup, profile, credentials
│   │   ├── upload.py              ← File upload with security hardening
│   │   ├── analysis.py            ← Trigger AI analysis
│   │   ├── stl.py                 ← STL file serving
│   │   ├── export.py              ← DICOM export
│   │   └── volume.py              ← Volume test (disabled in prod)
│   ├── services/
│   │   ├── analysis_service.py    ← Full AI pipeline orchestrator
│   │   ├── segmentation.py        ← Threshold seg + 9-region partition
│   │   ├── preprocess_volume.py   ← Normalise volume
│   │   ├── metrics.py             ← Voxel count, volume calculation
│   │   ├── stl_exporter.py        ← numpy-stl export
│   │   ├── visualization.py       ← Segmentation preview PNG
│   │   ├── report_generator.py    ← JSON clinical report
│   │   ├── dicom_reader.py        ← Read DICOM metadata
│   │   └── nifti_reader.py        ← Read NIfTI metadata
│   ├── auth/
│   │   └── jwt_handler.py         ← JWT create/verify, require_auth
│   ├── database/
│   │   ├── connection.py          ← MySQL connection helper
│   │   └── scan_repository.py     ← save_scan(), get_scan()
│   └── static/                    ← HTML pages served by FastAPI
│       ├── login.html, signup.html, dashboard.html
│       ├── upload.html, results.html, history.html
│       ├── workflow.html, viewer.html, refine.html
│       └── forgot-password.html, reset-password.html
│
├── dental-ai-frontend/            ← React 18 + Vite + TypeScript SPA
│   └── src/
│       ├── main.tsx               ← Router setup, 8 routes
│       ├── pages/                 ← LoginPage, Dashboard, Upload, etc.
│       └── lib/                   ← API client, store
│
├── DentAI-Mobile/                 ← React Native 0.76.5 App
│   └── src/
│       ├── api/client.ts          ← All API endpoint wrappers
│       ├── screens/               ← All 8 mobile screens
│       ├── navigation/            ← Stack navigator
│       └── context/               ← AuthContext
│
├── Dental-segment-frontend/       ← Android Native (Kotlin) App
│   └── Dental-segment-app.apk    ← Compiled APK
│
├── automation/                    ← Selenium + pytest automation
│   ├── tests/
│   │   ├── conftest.py            ← Fixtures, JSON result saving
│   │   ├── test_authentication.py
│   │   ├── test_forms.py
│   │   ├── test_navigation.py
│   │   ├── test_ui_validation.py
│   │   └── test_regression.py
│   ├── pages/                     ← Page Object Model classes
│   ├── utils/
│   │   ├── report_generator.py    ← Excel + HTML report builder
│   │   ├── generate_automation_report.py ← Standalone demo runner
│   │   ├── driver_factory.py
│   │   ├── screenshot.py
│   │   └── waits.py
│   ├── config/settings.py         ← BASE_URL, paths, credentials
│   └── data/test_data.py
│
├── Vulnerability Test Results/    ← Manual security testing artifacts
│   ├── backend-inventory.md       ← Enumerated endpoints + findings
│   └── test-cases.xlsx            ← Manual security test cases
│
├── .github/workflows/
│   ├── deploy-and-test.yml        ← Main CI/CD pipeline
│   └── security-review.yml        ← Security scanning pipeline
│
└── setup_db.py                    ← MySQL schema initialisation script
```

---

## 12. Key Configuration

### Environment Variables (backend)
```
DEBUG_MODE=false          # Set true to enable Swagger/docs
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
JWT_SECRET_KEY=<secret>   # Used to sign JWT tokens
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=dental_ai
```

### Test Credentials (automation config)
```
TEST_EMAIL=doctor@dental-ai-test.com
TEST_PASSWORD=TestPass123!
ADMIN_EMAIL=admin@dental-ai-test.com
ADMIN_PASSWORD=AdminPass123!
```

### Mobile App Base URL
```
BASE_URL = 'http://172.23.51.65:8000'   # LAN IP for physical device testing
```

---

## 13. Key Design Decisions

- **No ML model** — segmentation uses threshold-based + geometric partitioning (deterministic, no GPU required, fast)
- **JWT stateless auth** — no sessions on the server, token stored in browser localStorage / AsyncStorage
- **Single codebase, three frontends** — same FastAPI backend serves the static HTML app, the React SPA, and the React Native mobile app
- **Page Object Model** — automation tests use POM so page selectors are centralised and tests stay readable
- **Excel as primary CI artifact** — test results are always exported to `.xlsx` via openpyxl, available for 90 days in GitHub Actions regardless of whether the live site was reachable
- **ARGB color format** — openpyxl requires 8-character ARGB hex colors (`FF28A745` not `28A745`) — all colors in `report_generator.py` use the `FF` alpha prefix
- **Security-first uploads** — file uploads validate extension, MIME type (magic bytes), size (100 MB), filename (sanitised), and zip entries (Zip Slip prevention) before any processing

---

## 14. Glossary

| Term | Meaning in this project |
|------|------------------------|
| CBCT | Cone Beam Computed Tomography — the type of dental scan this app processes |
| DICOM | Digital Imaging and Communications in Medicine — standard medical scan file format |
| NIfTI | Neuroimaging Informatics Technology Initiative — another medical volume format (.nii, .nii.gz) |
| STL | Stereolithography — 3D mesh file format used for surgical planning and 3D printing |
| Mandible | The lower jaw bone — the anatomical structure being segmented |
| Condylar head | The rounded top of the jaw that connects to the skull (L/R) |
| Coronoid process | The triangular projection on the mandible (L/R) |
| Angle/Ramus | The ascending part of the jaw (L/R) |
| Body | The horizontal part of the lower jaw (L/R) |
| Symphyseal/Parasymphyseal | The front-centre region of the chin |
| IDOR | Insecure Direct Object Reference — accessing another user's data by changing an ID |
| Zip Slip | Attack where a malicious zip entry escapes the extraction directory via `../` paths |
| POM | Page Object Model — design pattern where each UI page has a Python class |
| ARGB | Alpha-Red-Green-Blue — 8-character hex color format required by openpyxl |
| JWT | JSON Web Token — stateless auth token signed with a secret key |
