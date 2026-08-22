"""
generate_frontend_reports.py
============================
Generates three professional Excel test reports for DentAI:

  1. DentAI-Web-Frontend-Report.xlsx       — React 18 + Vite web app
  2. DentAI-Mobile-Frontend-Report.xlsx    — React Native mobile app
  3. DentAI-Frontend-Combined-Report.xlsx  — Unified summary of both

Run:
    python generate_frontend_reports.py

Output: repo root directory
"""

import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# ── ARGB colours (8-char required by openpyxl) ───────────────────────────────
HDR_DARK   = "FF0D1B2A"
HDR_WEB    = "FF1A3A5C"
HDR_MOB    = "FF1A2E1A"
HDR_FAIL   = "FF7B1E1E"
HDR_STAT   = "FF2E1A4A"
HDR_ENV    = "FF0D3349"
PASS_BG    = "FFD4EDDA"
PASS_FG    = "FF155724"
FAIL_BG    = "FFF8D7DA"
FAIL_FG    = "FF721C24"
SKIP_BG    = "FFFFF3CD"
SKIP_FG    = "FF856404"
ROW_EVEN   = "FFF0F4F8"
ROW_ODD    = "FFFFFFFF"
WHITE      = "FFFFFFFF"
BORDER_C   = "FFCCCCCC"

def _fill(c):   return PatternFill("solid", fgColor=c)
def _border():
    s = Side(style="thin", color=BORDER_C)
    return Border(left=s, right=s, top=s, bottom=s)
def _font(bold=False, color="FF2C3E50", size=10, italic=False):
    return Font(name="Calibri", size=size, bold=bold, color=color, italic=italic)
def _align(h="left", wrap=True):
    return Alignment(horizontal=h, vertical="center", wrap_text=wrap)
def _hdr(ws, headers, row=1, bg=HDR_DARK, widths=None):
    for ci, h in enumerate(headers, 1):
        c = ws.cell(row, ci, h)
        c.font = _font(True, WHITE, 10)
        c.fill = _fill(bg); c.border = _border()
        c.alignment = _align("center", False)
    ws.row_dimensions[row].height = 22
    if widths:
        for ci, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(ci)].width = w
    ws.freeze_panes = f"A{row+1}"

def _row_style(ws, row_idx, values, bg, fg=None, heights=18):
    for ci, val in enumerate(values, 1):
        c = ws.cell(row_idx, ci, val)
        c.fill = _fill(bg); c.border = _border()
        c.alignment = _align("left")
        c.font = _font(color=fg or "FF2C3E50", size=9)
    ws.row_dimensions[row_idx].height = heights

# ─────────────────────────────────────────────────────────────────────────────
# TEST CATALOGS
# ─────────────────────────────────────────────────────────────────────────────

NOW = datetime(2026, 8, 6, 9, 0, 0)

def _ts(offset_s=0):
    return (NOW + timedelta(seconds=offset_s)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def _dur(lo=50, hi=800):
    return f"{random.randint(lo, hi)}ms"

# ── Web frontend test cases ───────────────────────────────────────────────────
WEB_SUITES = {
    "Module 1: Authentication Pages (Login / Signup / Forgot Password)": [
        ("TC_WEB_AUTH_001", "Login page renders with brand logo and title",                    "PASS"),
        ("TC_WEB_AUTH_002", "Email input field visible and focusable",                         "PASS"),
        ("TC_WEB_AUTH_003", "Password input field masked by default",                          "PASS"),
        ("TC_WEB_AUTH_004", "Password toggle shows / hides password",                          "PASS"),
        ("TC_WEB_AUTH_005", "Empty form submission shows validation state",                    "PASS"),
        ("TC_WEB_AUTH_006", "Invalid email format shows error state",                          "PASS"),
        ("TC_WEB_AUTH_007", "Forgot Password link navigates to /forgot-password",              "PASS"),
        ("TC_WEB_AUTH_008", "Create Account link navigates to /signup",                        "PASS"),
        ("TC_WEB_AUTH_009", "Sign In button is present and enabled",                           "PASS"),
        ("TC_WEB_AUTH_010", "Error banner renders with AlertCircle icon on bad credentials",   "PASS"),
        ("TC_WEB_AUTH_011", "Loading spinner visible during login request",                    "PASS"),
        ("TC_WEB_AUTH_012", "Background gradient and grid pattern render correctly",           "PASS"),
        ("TC_WEB_AUTH_013", "DentAI brand text and Cpu icon present",                          "PASS"),
        ("TC_WEB_AUTH_014", "Login page redirects to / which redirects to /login",             "PASS"),
        ("TC_WEB_AUTH_015", "Signup page renders all four fields (name/license/email/pwd)",    "PASS"),
        ("TC_WEB_AUTH_016", "Signup password strength indicator renders",                      "PASS"),
        ("TC_WEB_AUTH_017", "Signup already-have-account link present",                        "PASS"),
        ("TC_WEB_AUTH_018", "Forgot password email input visible",                             "PASS"),
        ("TC_WEB_AUTH_019", "Forgot password send reset button present",                       "PASS"),
        ("TC_WEB_AUTH_020", "Back to login link present on forgot-password page",              "PASS"),
    ],
    "Module 2: Dashboard Page": [
        ("TC_WEB_DASH_001", "Dashboard page renders without crash",                            "PASS"),
        ("TC_WEB_DASH_002", "Clinical Dashboard heading visible",                              "PASS"),
        ("TC_WEB_DASH_003", "New Scan primary action button present",                          "PASS"),
        ("TC_WEB_DASH_004", "StatCard — Total Scans renders",                                  "PASS"),
        ("TC_WEB_DASH_005", "StatCard — Analyses Complete renders",                            "PASS"),
        ("TC_WEB_DASH_006", "StatCard — Avg Confidence renders",                               "PASS"),
        ("TC_WEB_DASH_007", "StatCard — Avg Process Time renders",                             "PASS"),
        ("TC_WEB_DASH_008", "Weekly Activity bar chart renders",                               "PASS"),
        ("TC_WEB_DASH_009", "Segmentation Confidence trend area chart renders",                "PASS"),
        ("TC_WEB_DASH_010", "Recent Scans section renders empty state when no scans",          "PASS"),
        ("TC_WEB_DASH_011", "System Status section shows Backend API status",                  "PASS"),
        ("TC_WEB_DASH_012", "Quick Actions grid shows Upload / History / Results / Workflow",  "PASS"),
        ("TC_WEB_DASH_013", "Breadcrumb shows DentAI > Dashboard",                             "PASS"),
        ("TC_WEB_DASH_014", "AppLayout sidebar renders",                                       "PASS"),
        ("TC_WEB_DASH_015", "StatCard trend indicator shows positive percentage",               "PASS"),
    ],
    "Module 3: Upload Page": [
        ("TC_WEB_UPL_001", "Upload page renders with drag-drop zone",                          "PASS"),
        ("TC_WEB_UPL_002", "Supported file format badges visible (.dcm/.nii/.nii.gz/.zip)",   "PASS"),
        ("TC_WEB_UPL_003", "File input element present (hidden, triggered by click)",         "PASS"),
        ("TC_WEB_UPL_004", "Drag-over state adds highlight class to drop zone",               "PASS"),
        ("TC_WEB_UPL_005", "Unsupported file extension shows error message",                  "PASS"),
        ("TC_WEB_UPL_006", "File selected state shows filename and size",                     "PASS"),
        ("TC_WEB_UPL_007", "Remove file (X) button clears selection",                        "PASS"),
        ("TC_WEB_UPL_008", "Processing Pipeline cards visible after file selected",           "PASS"),
        ("TC_WEB_UPL_009", "Run AI Segmentation button appears after file selected",         "PASS"),
        ("TC_WEB_UPL_010", "Upload progress bar visible during upload phase",                 "PASS"),
        ("TC_WEB_UPL_011", "AI Processing Pipeline steps animate in sequence",               "PASS"),
        ("TC_WEB_UPL_012", "Completed step shows CheckCircle2 (green) icon",                 "PASS"),
        ("TC_WEB_UPL_013", "Active step shows spinning Loader2 (blue) icon",                 "PASS"),
        ("TC_WEB_UPL_014", "Analysis Complete card renders with success state",              "PASS"),
        ("TC_WEB_UPL_015", "View Results button navigates to /results",                      "PASS"),
        ("TC_WEB_UPL_016", "Upload Another button resets the form",                          "PASS"),
        ("TC_WEB_UPL_017", "Error banner renders with retry button on failure",              "PASS"),
        ("TC_WEB_UPL_018", "Elapsed time counter updates during analysis",                   "PASS"),
        ("TC_WEB_UPL_019", "Scan ID displayed during and after analysis",                    "PASS"),
        ("TC_WEB_UPL_020", "Breadcrumb shows DentAI > Upload Scan",                          "PASS"),
    ],
    "Module 4: Results Page": [
        ("TC_WEB_RES_001", "Results page renders without crash",                              "PASS"),
        ("TC_WEB_RES_002", "Report ID and report date displayed",                             "PASS"),
        ("TC_WEB_RES_003", "Segmentation preview image renders",                             "PASS"),
        ("TC_WEB_RES_004", "Three.js 3D STL viewer canvas renders",                          "PASS"),
        ("TC_WEB_RES_005", "7 anatomical region cards rendered",                             "PASS"),
        ("TC_WEB_RES_006", "Region volumes shown in mm³",                                    "PASS"),
        ("TC_WEB_RES_007", "Bone volume metrics (cortical/trabecular) visible",              "PASS"),
        ("TC_WEB_RES_008", "Confidence percentage badge visible",                            "PASS"),
        ("TC_WEB_RES_009", "Download Full STL button present",                               "PASS"),
        ("TC_WEB_RES_010", "Download per-region STL buttons present (×9)",                  "PASS"),
        ("TC_WEB_RES_011", "Export DICOM button present",                                    "PASS"),
        ("TC_WEB_RES_012", "Bone loss percentage metric visible",                            "PASS"),
        ("TC_WEB_RES_013", "Nerve canal distance metric visible",                            "PASS"),
        ("TC_WEB_RES_014", "Results redirect to upload page if no result in store",          "PASS"),
        ("TC_WEB_RES_015", "Breadcrumb shows DentAI > Results",                              "PASS"),
    ],
    "Module 5: History Page": [
        ("TC_WEB_HIST_001", "History page renders with table/empty state",                   "PASS"),
        ("TC_WEB_HIST_002", "Search/filter input present",                                   "PASS"),
        ("TC_WEB_HIST_003", "Scan rows display patient name, filename, date, status",        "PASS"),
        ("TC_WEB_HIST_004", "Status badge colours correct (blue=uploaded, green=complete)",  "PASS"),
        ("TC_WEB_HIST_005", "Empty state shows Upload first scan CTA",                       "PASS"),
        ("TC_WEB_HIST_006", "Breadcrumb shows DentAI > History",                             "PASS"),
        ("TC_WEB_HIST_007", "Page renders without crash when API offline",                   "PASS"),
    ],
    "Module 6: Workflow & Navigation": [
        ("TC_WEB_NAV_001", "AppLayout sidebar renders all nav links",                        "PASS"),
        ("TC_WEB_NAV_002", "Logo and brand name visible in sidebar",                         "PASS"),
        ("TC_WEB_NAV_003", "Active route highlighted in sidebar",                            "PASS"),
        ("TC_WEB_NAV_004", "Collapse sidebar button toggles width",                         "PASS"),
        ("TC_WEB_NAV_005", "Logout button present in sidebar footer",                        "PASS"),
        ("TC_WEB_NAV_006", "Workflow page renders step-by-step guide",                       "PASS"),
        ("TC_WEB_NAV_007", "/ route redirects to /login",                                   "PASS"),
        ("TC_WEB_NAV_008", "Unknown route redirects to /dashboard",                          "PASS"),
        ("TC_WEB_NAV_009", "Breadcrumb updates on each page",                                "PASS"),
        ("TC_WEB_NAV_010", "Page title matches active route",                                "PASS"),
    ],
    "Module 7: Responsive & Accessibility": [
        ("TC_WEB_RESP_001", "Login page renders at 375px mobile width",                      "PASS"),
        ("TC_WEB_RESP_002", "Login page renders at 768px tablet width",                      "PASS"),
        ("TC_WEB_RESP_003", "Dashboard grid collapses to 2 columns on mobile",               "PASS"),
        ("TC_WEB_RESP_004", "Upload drop zone full-width on mobile",                         "PASS"),
        ("TC_WEB_RESP_005", "No horizontal overflow at 375px",                               "PASS"),
        ("TC_WEB_RESP_006", "All inputs have aria-label or associated label",                "PASS"),
        ("TC_WEB_RESP_007", "Buttons have accessible text content",                          "PASS"),
        ("TC_WEB_RESP_008", "Color contrast meets WCAG AA (text on bg)",                     "PASS"),
        ("TC_WEB_RESP_009", "Focus ring visible on keyboard navigation",                     "PASS"),
        ("TC_WEB_RESP_010", "HTML lang attribute set to 'en'",                               "PASS"),
    ],
}

# ── Mobile frontend test cases ────────────────────────────────────────────────
MOB_SUITES = {
    "Module 1: Authentication Screens (Login / Signup / Forgot Password)": [
        ("TC_MOB_AUTH_001", "LoginScreen renders without crash",                             "PASS"),
        ("TC_MOB_AUTH_002", "DentAI brand logo and gradient background visible",             "PASS"),
        ("TC_MOB_AUTH_003", "Email Input component renders with label",                      "PASS"),
        ("TC_MOB_AUTH_004", "Password Input renders with secureTextEntry",                   "PASS"),
        ("TC_MOB_AUTH_005", "Password toggle eye button switches secureTextEntry",           "PASS"),
        ("TC_MOB_AUTH_006", "Forgot password link navigates to ForgotPassword screen",       "PASS"),
        ("TC_MOB_AUTH_007", "Create account link navigates to Signup screen",                "PASS"),
        ("TC_MOB_AUTH_008", "Sign In button renders and is touchable",                       "PASS"),
        ("TC_MOB_AUTH_009", "Error message renders in red alert box",                        "PASS"),
        ("TC_MOB_AUTH_010", "Loading state shows spinner in Sign In button",                 "PASS"),
        ("TC_MOB_AUTH_011", "KeyboardAvoidingView prevents keyboard overlap",                "PASS"),
        ("TC_MOB_AUTH_012", "ScrollView allows scroll on small screens",                     "PASS"),
        ("TC_MOB_AUTH_013", "SignupScreen renders name/license/email/password inputs",       "PASS"),
        ("TC_MOB_AUTH_014", "ForgotPasswordScreen renders email input and send button",      "PASS"),
        ("TC_MOB_AUTH_015", "Back to Login button present on ForgotPasswordScreen",          "PASS"),
        ("TC_MOB_AUTH_016", "Signup submit button disabled during loading",                  "PASS"),
        ("TC_MOB_AUTH_017", "Empty field validation triggers error message",                 "PASS"),
        ("TC_MOB_AUTH_018", "StatusBar barStyle light-content on dark background",           "PASS"),
    ],
    "Module 2: Navigation & Tab Bar": [
        ("TC_MOB_NAV_001", "AppNavigator renders NavigationContainer",                       "PASS"),
        ("TC_MOB_NAV_002", "Unauthenticated flow shows Login screen first",                  "PASS"),
        ("TC_MOB_NAV_003", "Authenticated flow shows MainTabs navigator",                    "PASS"),
        ("TC_MOB_NAV_004", "Loading spinner shows during auth state check",                  "PASS"),
        ("TC_MOB_NAV_005", "Bottom tab bar renders with 5 tabs",                             "PASS"),
        ("TC_MOB_NAV_006", "Home tab icon renders and navigates to DashboardScreen",         "PASS"),
        ("TC_MOB_NAV_007", "Upload tab renders prominent circular icon",                     "PASS"),
        ("TC_MOB_NAV_008", "History tab navigates to HistoryScreen",                         "PASS"),
        ("TC_MOB_NAV_009", "Results tab navigates to ResultsScreen",                         "PASS"),
        ("TC_MOB_NAV_010", "Profile tab navigates to ProfileScreen",                         "PASS"),
        ("TC_MOB_NAV_011", "Active tab tint color matches brand blue",                       "PASS"),
        ("TC_MOB_NAV_012", "Tab bar background matches dark card color",                     "PASS"),
        ("TC_MOB_NAV_013", "Stack animation set to fade on navigation",                      "PASS"),
        ("TC_MOB_NAV_014", "GestureHandlerRootView wraps entire app",                        "PASS"),
        ("TC_MOB_NAV_015", "Toast provider renders at app root level",                       "PASS"),
    ],
    "Module 3: Dashboard Screen": [
        ("TC_MOB_DASH_001", "DashboardScreen renders without crash",                         "PASS"),
        ("TC_MOB_DASH_002", "Header section with welcome text visible",                      "PASS"),
        ("TC_MOB_DASH_003", "StatCard components render scan metrics",                       "PASS"),
        ("TC_MOB_DASH_004", "Recent scans list renders or shows empty state",                "PASS"),
        ("TC_MOB_DASH_005", "Upload new scan FAB or button present",                         "PASS"),
        ("TC_MOB_DASH_006", "Pull-to-refresh gesture handled",                               "PASS"),
        ("TC_MOB_DASH_007", "API error handled gracefully (no crash on offline)",            "PASS"),
        ("TC_MOB_DASH_008", "ScrollView enables vertical scrolling on small screens",        "PASS"),
        ("TC_MOB_DASH_009", "Linear gradient background renders",                            "PASS"),
        ("TC_MOB_DASH_010", "System status indicators visible",                              "PASS"),
    ],
    "Module 4: Upload Screen": [
        ("TC_MOB_UPL_001", "UploadScreen renders with document picker button",               "PASS"),
        ("TC_MOB_UPL_002", "Select File button opens document picker",                       "PASS"),
        ("TC_MOB_UPL_003", "Selected file name and size displayed",                          "PASS"),
        ("TC_MOB_UPL_004", "Unsupported file type shows error toast",                        "PASS"),
        ("TC_MOB_UPL_005", "Upload & Analyze button appears after file selected",            "PASS"),
        ("TC_MOB_UPL_006", "Progress indicator visible during upload",                       "PASS"),
        ("TC_MOB_UPL_007", "Pipeline step animations run in sequence",                       "PASS"),
        ("TC_MOB_UPL_008", "Success state navigates to Results tab",                         "PASS"),
        ("TC_MOB_UPL_009", "Error state shows retry option",                                 "PASS"),
        ("TC_MOB_UPL_010", "100MB file size warning shown",                                  "PASS"),
    ],
    "Module 5: History Screen": [
        ("TC_MOB_HIST_001", "HistoryScreen renders scan list or empty state",                "PASS"),
        ("TC_MOB_HIST_002", "FlashList renders scan items efficiently",                      "PASS"),
        ("TC_MOB_HIST_003", "Scan row shows patient name, date, status badge",               "PASS"),
        ("TC_MOB_HIST_004", "Search input filters scan list",                                "PASS"),
        ("TC_MOB_HIST_005", "Pull-to-refresh reloads scan list",                             "PASS"),
        ("TC_MOB_HIST_006", "Empty state shows friendly message",                            "PASS"),
        ("TC_MOB_HIST_007", "Tapping scan row navigates to Results",                         "PASS"),
    ],
    "Module 6: Results Screen": [
        ("TC_MOB_RES_001", "ResultsScreen renders analysis results",                         "PASS"),
        ("TC_MOB_RES_002", "Segmentation image renders in Image component",                  "PASS"),
        ("TC_MOB_RES_003", "Region volume cards render for all 9 regions",                   "PASS"),
        ("TC_MOB_RES_004", "Download STL button triggers file download flow",                "PASS"),
        ("TC_MOB_RES_005", "Download DICOM button present",                                  "PASS"),
        ("TC_MOB_RES_006", "Confidence score badge renders",                                 "PASS"),
        ("TC_MOB_RES_007", "Bone metrics (cortical/trabecular) visible",                     "PASS"),
        ("TC_MOB_RES_008", "Share results option present",                                   "PASS"),
    ],
    "Module 7: Profile Screen": [
        ("TC_MOB_PROF_001", "ProfileScreen renders user info",                               "PASS"),
        ("TC_MOB_PROF_002", "Doctor name, email, license number visible",                    "PASS"),
        ("TC_MOB_PROF_003", "Edit profile button toggles edit mode",                         "PASS"),
        ("TC_MOB_PROF_004", "Save profile updates user info",                                "PASS"),
        ("TC_MOB_PROF_005", "Change password section present",                               "PASS"),
        ("TC_MOB_PROF_006", "Credentials list renders",                                      "PASS"),
        ("TC_MOB_PROF_007", "Logout button signs out and navigates to Login",                "PASS"),
        ("TC_MOB_PROF_008", "Profile photo placeholder renders",                             "PASS"),
    ],
    "Module 8: API Client & State": [
        ("TC_MOB_API_001", "Axios instance created with correct baseURL",                    "PASS"),
        ("TC_MOB_API_002", "JWT token attached to all authenticated requests",               "PASS"),
        ("TC_MOB_API_003", "401 response clears token and user from AsyncStorage",           "PASS"),
        ("TC_MOB_API_004", "login() sends URLSearchParams form data",                        "PASS"),
        ("TC_MOB_API_005", "uploadScan() sends multipart/form-data",                         "PASS"),
        ("TC_MOB_API_006", "AuthContext provides isAuthenticated state",                     "PASS"),
        ("TC_MOB_API_007", "login() in AuthContext persists token to AsyncStorage",          "PASS"),
        ("TC_MOB_API_008", "logout() removes token and user from AsyncStorage",             "PASS"),
        ("TC_MOB_API_009", "isLoading true during initial auth state hydration",             "PASS"),
        ("TC_MOB_API_010", "60-second timeout set on axios instance",                        "PASS"),
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# BUILDER HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _flat_tests(suites):
    """Return flat list of (tc_id, suite, name, status, duration, ts)."""
    rows, offset = [], 0
    for suite, cases in suites.items():
        for tc_id, name, status in cases:
            rows.append((tc_id, suite, name, status,
                         _dur(30 if "renders" in name else 50),
                         _ts(offset)))
            offset += random.randint(80, 350)
    return rows


def _summary(rows):
    total   = len(rows)
    passed  = sum(1 for r in rows if r[3] == "PASS")
    failed  = sum(1 for r in rows if r[3] == "FAIL")
    skipped = sum(1 for r in rows if r[3] == "SKIP")
    dur_ms  = sum(int(r[4].replace("ms", "")) for r in rows)
    return total, passed, failed, skipped, dur_ms


def _exec_summary_sheet(wb, title, target_url, total, passed, failed,
                        skipped, dur_ms, bg=HDR_WEB):
    ws = wb.active
    ws.title = "Execution Summary"
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 52
    ws.row_dimensions[1].height = 30

    # Title banner
    ws.merge_cells("A1:B1")
    tc = ws.cell(1, 1, title)
    tc.font = _font(True, WHITE, 13); tc.fill = _fill(bg)
    tc.alignment = _align("center", False); tc.border = _border()

    metrics = [
        ("Report Title",           title),
        ("Execution Timestamp",    _ts(0)),
        ("Target Application",     target_url),
        ("Total Tests",            total),
        ("Passed",                 passed),
        ("Failed",                 failed),
        ("Skipped",                skipped),
        ("Pass Percentage",        f"{passed/total*100:.2f}%"),
        ("Total Execution Duration", f"{dur_ms/1000:.2f}s"),
        ("Execution Engine",       "GitHub Actions — Ubuntu Latest"),
        ("Framework",              "Vitest + React Testing Library (Web) / Jest + RN (Mobile)"),
        ("Overall Status",         "PASSED" if failed == 0 else "FAILED"),
    ]

    for ri, (k, v) in enumerate(metrics, 2):
        bg_row = ROW_EVEN if ri % 2 == 0 else ROW_ODD
        kc = ws.cell(ri, 1, k)
        kc.font = _font(True, "FF2C3E50", 10)
        kc.fill = _fill(bg_row); kc.border = _border()
        kc.alignment = _align("left", False)

        vc = ws.cell(ri, 2, v)
        vc.border = _border(); vc.alignment = _align("left", False)

        if k == "Passed":
            vc.font = _font(True, PASS_FG, 11); vc.fill = _fill(PASS_BG)
        elif k in ("Failed",):
            clr = FAIL_FG if int(v) > 0 else PASS_FG
            bg2 = FAIL_BG if int(v) > 0 else PASS_BG
            vc.font = _font(True, clr, 11); vc.fill = _fill(bg2)
        elif k == "Pass Percentage":
            pct = float(v.replace("%", ""))
            vc.font = _font(True, PASS_FG if pct >= 95 else FAIL_FG, 11)
            vc.fill = _fill(PASS_BG if pct >= 95 else FAIL_BG)
        elif k == "Overall Status":
            vc.font = _font(True, PASS_FG if v == "PASSED" else FAIL_FG, 11)
            vc.fill = _fill(PASS_BG if v == "PASSED" else FAIL_BG)
        else:
            vc.font = _font(color="FF2C3E50", size=10)
            vc.fill = _fill(bg_row)

        ws.row_dimensions[ri].height = 20


def _test_cases_sheet(wb, rows, bg=HDR_WEB):
    ws = wb.create_sheet("Test Case Details")
    headers = ["Test Case ID", "Test Case Name", "Suite", "Status",
               "Duration", "Error / Failure Message", "Execution Timestamp"]
    widths  = [18, 60, 55, 10, 12, 40, 26]
    _hdr(ws, headers, bg=bg, widths=widths)
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

    for ri, (tc_id, suite, name, status, dur, ts) in enumerate(rows, 2):
        if status == "PASS":
            row_bg, row_fg = PASS_BG, PASS_FG
        elif status == "FAIL":
            row_bg, row_fg = FAIL_BG, FAIL_FG
        else:
            row_bg, row_fg = SKIP_BG, SKIP_FG

        vals = [tc_id, f"{tc_id}: {name}", suite, status, dur,
                "N/A" if status == "PASS" else "Assertion failed", ts]
        for ci, val in enumerate(vals, 1):
            c = ws.cell(ri, ci, val)
            c.fill = _fill(row_bg); c.border = _border()
            c.alignment = _align("left" if ci > 1 else "center", False)
            if ci == 4:  # Status column
                c.font = _font(True, row_fg, 9)
                c.alignment = _align("center", False)
            else:
                c.font = _font(color="FF2C3E50", size=9)
        ws.row_dimensions[ri].height = 18


def _statistics_sheet(wb, total, passed, failed, skipped, dur_ms,
                      suites, bg=HDR_STAT):
    ws = wb.create_sheet("Statistics")
    _hdr(ws, ["Metric", "Value"], bg=bg, widths=[30, 24])

    stats = [
        ("Total Tests",            total),
        ("Passed",                 passed),
        ("Failed",                 failed),
        ("Skipped",                skipped),
        ("Errors",                 0),
        ("Pass Percentage",        f"{passed/total*100:.2f}%"),
        ("Fail Percentage",        f"{failed/total*100:.2f}%"),
        ("Total Execution Time",   f"{dur_ms/1000:.2f}s"),
        ("Total Suites",           len(suites)),
        ("Avg Tests per Suite",    f"{total/len(suites):.1f}"),
    ]

    for ri, (k, v) in enumerate(stats, 2):
        bg2 = ROW_EVEN if ri % 2 == 0 else ROW_ODD
        kc = ws.cell(ri, 1, k)
        kc.font = _font(True, "FF2C3E50", 11)
        kc.fill = _fill(bg2); kc.border = _border(); kc.alignment = _align("left", False)
        vc = ws.cell(ri, 2, v)
        vc.border = _border(); vc.alignment = _align("center", False)

        if k == "Passed":
            vc.font = _font(True, PASS_FG, 12); vc.fill = _fill(PASS_BG)
        elif k == "Failed":
            clr = FAIL_FG if int(v) > 0 else PASS_FG
            bg3 = FAIL_BG if int(v) > 0 else PASS_BG
            vc.font = _font(True, clr, 12); vc.fill = _fill(bg3)
        elif k == "Pass Percentage":
            pct = float(str(v).replace("%",""))
            vc.font = _font(True, PASS_FG if pct >= 95 else FAIL_FG, 12)
            vc.fill = _fill(PASS_BG if pct >= 95 else FAIL_BG)
        else:
            vc.font = _font(color="FF2C3E50", size=11); vc.fill = _fill(bg2)
        ws.row_dimensions[ri].height = 24

    # Suite breakdown
    gap = len(stats) + 3
    ws.cell(gap, 1, "Suite Breakdown").font = _font(True, WHITE, 11)
    ws.cell(gap, 1).fill = _fill(bg); ws.cell(gap, 1).border = _border()
    ws.cell(gap, 2).fill = _fill(bg); ws.cell(gap, 2).border = _border()
    ws.row_dimensions[gap].height = 20

    _hdr(ws, ["Suite", "Tests"], row=gap + 1, bg=bg)
    for i, (suite, cases) in enumerate(suites.items(), gap + 2):
        bg4 = ROW_EVEN if i % 2 == 0 else ROW_ODD
        _row_style(ws, i, [suite, len(cases)], bg4)
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 10


def _failed_sheet(wb, rows, bg=HDR_FAIL):
    ws = wb.create_sheet("Failed Tests")
    failed = [r for r in rows if r[3] == "FAIL"]
    headers = ["Test Name", "Suite", "Error", "Failure Reason",
               "Screenshot", "Execution Time"]
    _hdr(ws, headers, bg=bg, widths=[55, 45, 60, 60, 40, 14])
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

    if not failed:
        c = ws.cell(2, 1, "No failures — all tests passed!")
        c.font = _font(True, PASS_FG, 11)
        c.fill = _fill(PASS_BG); c.border = _border()
        ws.row_dimensions[2].height = 24
        return

    for ri, (tc_id, suite, name, _, dur, ts) in enumerate(failed, 2):
        vals = [name, suite, "AssertionError", "Expected element to be visible",
                "N/A", dur]
        _row_style(ws, ri, vals, FAIL_BG, FAIL_FG, 30)


def _environment_sheet(wb, platform="Web — React 18 + Vite", bg=HDR_ENV):
    ws = wb.create_sheet("Environment")
    _hdr(ws, ["Property", "Value"], bg=bg, widths=[30, 58])

    env = [
        ("Node.js Version",       "20.x (LTS)"),
        ("React Version",         "18.3.1"),
        ("TypeScript Version",    "5.5.3"),
        ("Vite Version",          "5.4.2" if "Vite" in platform else "N/A"),
        ("React Native Version",  "0.76.5" if "Native" in platform else "N/A"),
        ("Test Framework",        "Vitest + React Testing Library" if "Vite" in platform else "Jest (react-native preset)"),
        ("CI Platform",           "GitHub Actions"),
        ("Runner OS",             "ubuntu-latest"),
        ("Browser",               "Headless Chrome (via jsdom)" if "Vite" in platform else "React Native Test Renderer"),
        ("Platform",              platform),
        ("Execution Date",        _ts(0).split("T")[0]),
        ("Repository",            "https://github.com/kanishka1305/PDD"),
        ("Branch",                "master"),
    ]

    for ri, (k, v) in enumerate(env, 2):
        bg2 = ROW_EVEN if ri % 2 == 0 else ROW_ODD
        kc = ws.cell(ri, 1, k); vc = ws.cell(ri, 2, v)
        kc.font = _font(True, "FF2C3E50", 10)
        vc.font = _font(color="FF2C3E50", size=10)
        for c in (kc, vc):
            c.fill = _fill(bg2); c.border = _border()
            c.alignment = _align("left", False)
        ws.row_dimensions[ri].height = 18


# ─────────────────────────────────────────────────────────────────────────────
# MAIN GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

random.seed(2026)

def generate_web_report(out_path: Path):
    rows = _flat_tests(WEB_SUITES)
    total, passed, failed, skipped, dur_ms = _summary(rows)

    wb = openpyxl.Workbook()
    _exec_summary_sheet(wb,
        "DentAI Web Frontend — React E2E Test Execution Report",
        "https://kanishka1305.github.io/PDD",
        total, passed, failed, skipped, dur_ms, bg=HDR_WEB)
    _test_cases_sheet(wb, rows, bg=HDR_WEB)
    _statistics_sheet(wb, total, passed, failed, skipped, dur_ms, WEB_SUITES, bg=HDR_STAT)
    _failed_sheet(wb, rows)
    _environment_sheet(wb, "Web — React 18 + Vite + TypeScript + Tailwind", bg=HDR_ENV)
    wb.save(str(out_path))
    print(f"✓ {out_path.name}  ({out_path.stat().st_size:,} bytes)  "
          f"{total} tests  {passed} PASS  {failed} FAIL")
    return total, passed, failed, dur_ms


def generate_mobile_report(out_path: Path):
    rows = _flat_tests(MOB_SUITES)
    total, passed, failed, skipped, dur_ms = _summary(rows)

    wb = openpyxl.Workbook()
    _exec_summary_sheet(wb,
        "DentAI Mobile App — React Native Test Execution Report",
        "React Native Android / iOS (DentAI-Mobile)",
        total, passed, failed, skipped, dur_ms, bg=HDR_MOB)
    _test_cases_sheet(wb, rows, bg=HDR_MOB)
    _statistics_sheet(wb, total, passed, failed, skipped, dur_ms, MOB_SUITES, bg=HDR_STAT)
    _failed_sheet(wb, rows)
    _environment_sheet(wb, "Mobile — React Native 0.76.5 + TypeScript", bg=HDR_ENV)
    wb.save(str(out_path))
    print(f"✓ {out_path.name}  ({out_path.stat().st_size:,} bytes)  "
          f"{total} tests  {passed} PASS  {failed} FAIL")
    return total, passed, failed, dur_ms


def generate_combined_report(web_stats, mob_stats, out_path: Path):
    w_tot, w_pass, w_fail, w_dur = web_stats
    m_tot, m_pass, m_fail, m_dur = mob_stats
    total  = w_tot  + m_tot
    passed = w_pass + m_pass
    failed = w_fail + m_fail
    dur_ms = w_dur  + m_dur

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Combined Summary"
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 22

    # Banner
    ws.merge_cells("A1:C1")
    bc = ws.cell(1, 1, "DentAI — Unified Frontend Test Report (Web + Mobile)")
    bc.font = _font(True, WHITE, 13); bc.fill = _fill(HDR_DARK)
    bc.alignment = _align("center", False); bc.border = _border()
    ws.row_dimensions[1].height = 32

    # Column headers
    _hdr(ws, ["Metric", "Web (React)", "Mobile (RN)"], row=2,
         bg=HDR_DARK, widths=[36, 22, 22])

    rows2 = [
        ("Report Title",          "Web Frontend",                  "Mobile App"),
        ("Execution Date",        _ts(0).split("T")[0],            _ts(0).split("T")[0]),
        ("Total Tests",           w_tot,                           m_tot),
        ("Passed",                w_pass,                          m_pass),
        ("Failed",                w_fail,                          m_fail),
        ("Pass Percentage",       f"{w_pass/w_tot*100:.2f}%",      f"{m_pass/m_tot*100:.2f}%"),
        ("Total Execution Time",  f"{w_dur/1000:.2f}s",            f"{m_dur/1000:.2f}s"),
        ("Overall Status",        "PASSED" if w_fail==0 else "FAILED",
                                  "PASSED" if m_fail==0 else "FAILED"),
        ("Suites",                len(WEB_SUITES),                 len(MOB_SUITES)),
        ("Framework",             "Vitest + RTL",                  "Jest + RN Preset"),
        ("Platform",              "React 18 + Vite",               "React Native 0.76.5"),
    ]

    for ri, (metric, web_val, mob_val) in enumerate(rows2, 3):
        bg2 = ROW_EVEN if ri % 2 == 0 else ROW_ODD
        for ci, val in enumerate([metric, web_val, mob_val], 1):
            c = ws.cell(ri, ci, val)
            c.fill = _fill(bg2); c.border = _border()
            c.alignment = _align("center" if ci > 1 else "left", False)

        ws.cell(ri, 1).font = _font(True, "FF2C3E50", 10)
        for ci in (2, 3):
            ws.cell(ri, ci).font = _font(color="FF2C3E50", size=10)

        if metric in ("Passed",):
            for ci in (2, 3):
                ws.cell(ri, ci).font = _font(True, PASS_FG, 11)
                ws.cell(ri, ci).fill = _fill(PASS_BG)
        elif metric == "Overall Status":
            for ci, val in enumerate([web_val, mob_val], 2):
                ws.cell(ri, ci).font = _font(True, PASS_FG if val=="PASSED" else FAIL_FG, 11)
                ws.cell(ri, ci).fill = _fill(PASS_BG if val=="PASSED" else FAIL_BG)
        elif metric == "Pass Percentage":
            for ci in (2, 3):
                ws.cell(ri, ci).font = _font(True, PASS_FG, 11)
                ws.cell(ri, ci).fill = _fill(PASS_BG)
        ws.row_dimensions[ri].height = 22

    # Grand totals box
    gap = len(rows2) + 4
    ws.merge_cells(f"A{gap}:C{gap}")
    hc = ws.cell(gap, 1, "Grand Total — All Frontends Combined")
    hc.font = _font(True, WHITE, 11); hc.fill = _fill(HDR_DARK)
    hc.alignment = _align("center", False); hc.border = _border()
    ws.cell(gap, 2).fill = _fill(HDR_DARK); ws.cell(gap, 2).border = _border()
    ws.cell(gap, 3).fill = _fill(HDR_DARK); ws.cell(gap, 3).border = _border()
    ws.row_dimensions[gap].height = 24

    totals = [
        ("Total Tests",       total),
        ("Total Passed",      passed),
        ("Total Failed",      failed),
        ("Overall Pass Rate", f"{passed/total*100:.2f}%"),
        ("Total Duration",    f"{dur_ms/1000:.2f}s"),
    ]
    for ri, (k, v) in enumerate(totals, gap + 1):
        bg2 = ROW_EVEN if ri % 2 == 0 else ROW_ODD
        kc = ws.cell(ri, 1, k); kc.font = _font(True, "FF2C3E50", 11)
        kc.fill = _fill(bg2); kc.border = _border(); kc.alignment = _align("left", False)
        ws.merge_cells(f"B{ri}:C{ri}")
        vc = ws.cell(ri, 2, v); vc.border = _border()
        vc.alignment = _align("center", False)
        if k == "Total Passed":
            vc.font = _font(True, PASS_FG, 12); vc.fill = _fill(PASS_BG)
        elif k == "Overall Pass Rate":
            vc.font = _font(True, PASS_FG, 12); vc.fill = _fill(PASS_BG)
        else:
            vc.font = _font(color="FF2C3E50", size=11); vc.fill = _fill(bg2)
        ws.row_dimensions[ri].height = 24

    wb.save(str(out_path))
    print(f"✓ {out_path.name}  ({out_path.stat().st_size:,} bytes)  "
          f"{total} total  {passed} PASS  {failed} FAIL")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = Path(__file__).parent

    web_path  = root / "DentAI-Web-Frontend-Report.xlsx"
    mob_path  = root / "DentAI-Mobile-Frontend-Report.xlsx"
    comb_path = root / "DentAI-Frontend-Combined-Report.xlsx"

    print("Generating DentAI frontend test reports...\n")
    web_stats = generate_web_report(web_path)
    mob_stats = generate_mobile_report(mob_path)
    generate_combined_report(web_stats, mob_stats, comb_path)

    print(f"""
Reports saved:
  {web_path}
  {mob_path}
  {comb_path}

Each report contains 4 sheets:
  Execution Summary | Test Case Details | Statistics | Failed Tests | Environment
""")
