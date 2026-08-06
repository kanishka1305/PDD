"""
generate_test_cases_excel.py
Generates DentAI_All_Test_Cases.xlsx from every test case in the automation suite.
Run: python generate_test_cases_excel.py
"""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# ── ARGB color constants (8-char required by openpyxl) ───────────────────────
C_HEADER    = "FF1A252F"   # dark navy
C_PASS      = "FF28A745"   # green
C_FAIL      = "FFDC3545"   # red
C_SKIP      = "FFFFC107"   # amber
C_AUTH      = "FF2980B9"   # blue
C_AUTHZ     = "FF8E44AD"   # purple
C_NAV       = "FF27AE60"   # emerald
C_UI        = "FF16A085"   # teal
C_FORM      = "FF2C3E50"   # dark
C_FILE      = "FFE67E22"   # orange
C_HIST      = "FF1ABC9C"   # green-teal
C_PROF      = "FFC0392B"   # crimson
C_REG       = "FF7F8C8D"   # grey
C_PERF      = "FF6C3483"   # violet
C_ACC       = "FF117A65"   # dark teal
C_RESP      = "FF1F618D"   # steel blue
C_ROW_EVEN  = "FFECF0F1"
C_ROW_ODD   = "FFFFFFFF"
C_WHITE     = "FFFFFFFF"

def bdr():
    s = Side(style="thin", color="FFCCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

def fill(c):
    return PatternFill("solid", fgColor=c)

def hdr_font(color=C_WHITE):
    return Font(name="Calibri", size=10, bold=True, color=color)

def cell_font(bold=False):
    return Font(name="Calibri", size=9, bold=bold, color="FF2C3E50")

def cen():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def lft():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

# ── ALL TEST CASES ────────────────────────────────────────────────────────────
# Format: (TC_ID, Module, Test_Name, Objective, Precondition, Steps, Expected, Priority, Status)

ALL_TESTS = []

# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION  (TC-AUTH-001 … 040)
# ═══════════════════════════════════════════════════════════════════════════════
AUTH = [
  ("TC-AUTH-001","Authentication","Login page loads","Verify login page loads from GitHub Pages","Browser open","Navigate to /login.html","Page loads, title not empty","Critical","Active"),
  ("TC-AUTH-002","Authentication","Email field visible","Email input is present on login page","Login page open","Inspect email input","Email field visible","Critical","Active"),
  ("TC-AUTH-003","Authentication","Password field visible","Password input is present","Login page open","Inspect password input","Password field visible","Critical","Active"),
  ("TC-AUTH-004","Authentication","Login button visible","Submit button is present","Login page open","Inspect submit button","Login button visible","Critical","Active"),
  ("TC-AUTH-005","Authentication","Signup link visible","Signup link present on login page","Login page open","Inspect signup link","Link visible","High","Active"),
  ("TC-AUTH-006","Authentication","Password field masked","Password type=password","Login page open","Check input type","type='password'","Critical","Active"),
  ("TC-AUTH-007","Authentication","Login form present","Form element exists","Login page open","Inspect DOM","Form found","High","Active"),
  ("TC-AUTH-008","Authentication","Empty email validation","HTML5 required stops submission","Login page open","Leave email empty, submit","Stays on login page","High","Active"),
  ("TC-AUTH-009","Authentication","Empty password validation","HTML5 required stops submission","Login page open","Leave password empty, submit","Stays on login page","High","Active"),
  ("TC-AUTH-010","Authentication","Both fields empty","Both empty handled gracefully","Login page open","Submit empty form","Stays on login page","High","Active"),
  ("TC-AUTH-011","Authentication","Invalid email format","Bad email format rejected","Login page open","Enter 'notanemail', submit","Stays on login page","High","Active"),
  ("TC-AUTH-012","Authentication","Wrong credentials error","Wrong creds show error or stay","Login page open","Enter wrong creds, submit","No dashboard access","Critical","Active"),
  ("TC-AUTH-013","Authentication","SQL injection email","SQLi bypasses rejected","Login page open","Enter SQL payload","Stays on login page","Critical","Active"),
  ("TC-AUTH-014","Authentication","XSS in email","XSS payload not executed","Login page open","Enter <script>alert, submit","XSS not in source","Critical","Active"),
  ("TC-AUTH-015","Authentication","Very long email","500-char email handled","Login page open","Enter 500-char email, submit","No crash","Medium","Active"),
  ("TC-AUTH-016","Authentication","Forgot password link","Forgot link present","Login page open","Inspect forgot link","Link present","Medium","Active"),
  ("TC-AUTH-017","Authentication","Signup link navigates","Click signup navigates","Login page open","Click signup link","URL contains signup","High","Active"),
  ("TC-AUTH-018","Authentication","Signup page loads","Signup page loads","Browser open","Navigate to /signup.html","Page title not empty","Critical","Active"),
  ("TC-AUTH-019","Authentication","Signup has all fields","All required fields present","Signup page open","Inspect all inputs","Name, email, pwd, license visible","Critical","Active"),
  ("TC-AUTH-020","Authentication","Signup empty name","Empty name blocked","Signup page open","Leave name empty, submit","Stays on signup","High","Active"),
  ("TC-AUTH-021","Authentication","Signup empty email","Empty email blocked","Signup page open","Leave email empty, submit","Stays on signup","High","Active"),
  ("TC-AUTH-022","Authentication","Signup empty password","Empty password blocked","Signup page open","Leave pwd empty, submit","Stays on signup","High","Active"),
  ("TC-AUTH-023","Authentication","Signup invalid email","Invalid email format rejected","Signup page open","Enter bad email, submit","Stays on signup","High","Active"),
  ("TC-AUTH-024","Authentication","Signup weak password","Weak password rejected","Signup page open","Enter '123', submit","Stays on signup","High","Active"),
  ("TC-AUTH-025","Authentication","XSS in signup name","XSS in name not executed","Signup page open","Enter <script> in name, submit","XSS not in source","Critical","Active"),
  ("TC-AUTH-026","Authentication","Forgot password page loads","Page loads","Browser open","Navigate to /forgot-password.html","Page loads","High","Active"),
  ("TC-AUTH-027","Authentication","Forgot pwd email field","Email field present","Forgot pwd page open","Inspect email input","Email field visible","High","Active"),
  ("TC-AUTH-028","Authentication","Forgot pwd empty submit","Empty submit stays on page","Forgot pwd page open","Submit empty","No crash","Medium","Active"),
  ("TC-AUTH-029","Authentication","Forgot pwd invalid email","Invalid email handled","Forgot pwd page open","Enter bad email, submit","No crash","Medium","Active"),
  ("TC-AUTH-030","Authentication","Forgot pwd no user enum","No user enumeration","Forgot pwd page open","Enter unknown email","Generic or no message","Critical","Active"),
  ("TC-AUTH-031","Authentication","Login page title","Title not empty","Browser open","Load login page","Title.length > 0","High","Active"),
  ("TC-AUTH-032","Authentication","Signup has login link","Login link on signup","Signup page open","Inspect login link","Link present","Medium","Active"),
  ("TC-AUTH-033","Authentication","Login loads under 5s","Performance check","Browser open","Time page load","< 5 seconds","High","Active"),
  ("TC-AUTH-034","Authentication","Signup loads under 5s","Performance check","Browser open","Time page load","< 5 seconds","High","Active"),
  ("TC-AUTH-035","Authentication","No console errors login","No SEVERE browser errors","Login page open","Check browser logs","0 SEVERE errors","Medium","Active"),
  ("TC-AUTH-036","Authentication","Login page HTTPS","HTTPS enforced","Browser open","Check URL scheme","Starts with https://","Critical","Active"),
  ("TC-AUTH-037","Authentication","Email autocomplete","Autocomplete not disabled","Login page open","Check autocomplete attr","Not 'off'","Low","Active"),
  ("TC-AUTH-038","Authentication","Password type=password","Password masking enforced","Login page open","Check input type","type='password'","Critical","Active"),
  ("TC-AUTH-039","Authentication","Login mobile 375px","Renders on mobile","375x667 viewport","Load login page","Email + button visible","High","Active"),
  ("TC-AUTH-040","Authentication","Login tablet 768px","Renders on tablet","768x1024 viewport","Load login page","Email field visible","Medium","Active"),
]
ALL_TESTS.extend(AUTH)

# ═══════════════════════════════════════════════════════════════════════════════
# AUTHORIZATION / SECURITY  (TC-AUTHZ-001 … 040)
# ═══════════════════════════════════════════════════════════════════════════════
AUTHZ = [
  ("TC-AUTHZ-001","Authorization","Dashboard requires login","Unauthenticated redirect","No session","Navigate to /dashboard.html","Redirect or no data","Critical","Active"),
  ("TC-AUTHZ-002","Authorization","Upload requires login","Unauthenticated redirect","No session","Navigate to /upload.html","Redirect or no data","Critical","Active"),
  ("TC-AUTHZ-003","Authorization","History requires login","Unauthenticated redirect","No session","Navigate to /history.html","Redirect or no data","Critical","Active"),
  ("TC-AUTHZ-004","Authorization","Results requires login","Unauthenticated redirect","No session","Navigate to /results.html","Redirect or no data","Critical","Active"),
  ("TC-AUTHZ-005","Authorization","Viewer requires login","Unauthenticated redirect","No session","Navigate to /viewer.html","Redirect or no data","Critical","Active"),
  ("TC-AUTHZ-006","Authorization","Workflow requires login","Unauthenticated redirect","No session","Navigate to /workflow.html","Redirect or no data","High","Active"),
  ("TC-AUTHZ-007","Authorization","Refine requires login","Unauthenticated redirect","No session","Navigate to /refine.html","Redirect or no data","High","Active"),
  ("TC-AUTHZ-008","Authorization","Login page is public","Login accessible without auth","No session","Navigate to /login.html","Page loads","Critical","Active"),
  ("TC-AUTHZ-009","Authorization","Signup page is public","Signup accessible without auth","No session","Navigate to /signup.html","Page loads","Critical","Active"),
  ("TC-AUTHZ-010","Authorization","Forgot pwd is public","Forgot password accessible","No session","Navigate to /forgot-password.html","Page loads","High","Active"),
  ("TC-AUTHZ-011","Authorization","No API keys in source","No secrets in HTML","Login page open","Inspect page source","No 'sk-' or api_key","Critical","Active"),
  ("TC-AUTHZ-012","Authorization","No passwords in source","No plaintext passwords","Login page open","Inspect page source","No password= in HTML","Critical","Active"),
  ("TC-AUTHZ-013","Authorization","No tokens in source","No bearer tokens in HTML","Login page open","Inspect page source","No 'bearer ' in HTML","Critical","Active"),
  ("TC-AUTHZ-014","Authorization","HTTPS enforced","All pages HTTPS","Browser open","Load login, check URL","Starts with https://","Critical","Active"),
  ("TC-AUTHZ-015","Authorization","No admin panel","Admin panel not exposed","Browser open","Navigate to /admin","No admin access","High","Active"),
  ("TC-AUTHZ-016","Authorization","No phpMyAdmin","DB admin not exposed","Browser open","Navigate to /phpmyadmin","Not accessible","High","Active"),
  ("TC-AUTHZ-017","Authorization","Form POST method","Form not using GET","Login page open","Check form method","method=POST or empty","High","Active"),
  ("TC-AUTHZ-018","Authorization","No sensitive HTML comments","No credentials in comments","Login page open","Inspect source comments","No password/secret comments","Critical","Active"),
  ("TC-AUTHZ-019","Authorization","No debug info exposed","No stack traces","Login page open","Inspect page source","No 'traceback' in source","High","Active"),
  ("TC-AUTHZ-020","Authorization","All links HTTPS","No HTTP links on login","Login page open","Inspect all anchor hrefs","No http:// links","High","Active"),
  ("TC-AUTHZ-021","Authorization","Direct scan URL no data","Results need auth","No session","Navigate to /results.html?scan_id=1","No patient data shown","Critical","Active"),
  ("TC-AUTHZ-022","Authorization","Login has no user data","No real data on login page","Login page open","Inspect source","No patient_id in source","Critical","Active"),
  ("TC-AUTHZ-023","Authorization","Signup has no user data","No real data on signup","Signup page open","Inspect source","No patient_id in source","High","Active"),
  ("TC-AUTHZ-024","Authorization","History no data unauthed","No scan data without auth","No session","Load /history.html","No scan records visible","Critical","Active"),
  ("TC-AUTHZ-025","Authorization","Viewer no data unauthed","No 3D data without auth","No session","Load /viewer.html","No scan data visible","Critical","Active"),
  ("TC-AUTHZ-026","Authorization","Cookie Secure flag","Cookies have Secure flag","HTTPS site","Inspect cookies","Secure flag set","Critical","Active"),
  ("TC-AUTHZ-027","Authorization","Cookie HttpOnly flag","Session cookies HttpOnly","HTTPS site","Inspect session cookies","httpOnly set","Critical","Active"),
  ("TC-AUTHZ-028","Authorization","No directory listing","Uploads folder not browseable","Browser open","Navigate to /uploads/","No directory listing","Critical","Active"),
  ("TC-AUTHZ-029","Authorization",".env not accessible","Secrets file not public","Browser open","Navigate to /.env","No DB credentials","Critical","Active"),
  ("TC-AUTHZ-030","Authorization",".git not accessible","Git history not public","Browser open","Navigate to /.git/config","No [core] section","Critical","Active"),
  ("TC-AUTHZ-031","Authorization","Signup form action HTTPS","Form not posting to HTTP","Signup page open","Check form action","Not http://","High","Active"),
  ("TC-AUTHZ-032","Authorization","No server version in HTML","Server fingerprint hidden","Login page open","Inspect source","No 'uvicorn' in HTML","Medium","Active"),
  ("TC-AUTHZ-033","Authorization","No internal IPs in source","LAN IPs not exposed","Login page open","Regex scan source","No 192.168.x.x etc","High","Active"),
  ("TC-AUTHZ-034","Authorization","Signup duplicate prevention","Duplicate email handled","Signup page open","Submit duplicate email","Error shown or stay","High","Active"),
  ("TC-AUTHZ-035","Authorization","No user enumeration","Same response for valid/invalid","Forgot pwd page open","Submit valid then invalid email","Same message or none","Critical","Active"),
  ("TC-AUTHZ-036","Authorization","Back button security","Back btn shows no data after logout","Dashboard then login","Press back","No protected data","High","Active"),
  ("TC-AUTHZ-037","Authorization","No SQL in page source","No raw SQL queries exposed","Login page open","Search source for SELECT *","Not found","Critical","Active"),
  ("TC-AUTHZ-038","Authorization","No Python traceback","No traceback on any page","Login/signup open","Load pages","No 'Traceback' string","High","Active"),
  ("TC-AUTHZ-039","Authorization","CSP meta tag check","Content Security Policy present","Login page open","Inspect meta tags","CSP meta or header present","Medium","Active"),
  ("TC-AUTHZ-040","Authorization","All pages use HTTPS","HTTPS across all pages","Browser open","Load all 4 main pages","All https://","Critical","Active"),
]
ALL_TESTS.extend(AUTHZ)

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION  (TC-NAV-001 … 030)
# ═══════════════════════════════════════════════════════════════════════════════
NAV = [
  ("TC-NAV-001","Navigation","Home redirects to login","/ redirects correctly","Browser open","Navigate to /","Login page or main page shown","High","Active"),
  ("TC-NAV-002","Navigation","Login page direct URL","Login accessible via URL","Browser open","Navigate to /login.html","Page loads HTTPS","Critical","Active"),
  ("TC-NAV-003","Navigation","Signup page direct URL","Signup accessible via URL","Browser open","Navigate to /signup.html","Page loads HTTPS","High","Active"),
  ("TC-NAV-004","Navigation","Forgot pwd direct URL","Forgot pwd accessible","Browser open","Navigate to /forgot-password.html","Page loads HTTPS","High","Active"),
  ("TC-NAV-005","Navigation","Dashboard direct URL","Dashboard responds","Browser open","Navigate to /dashboard.html","Page loads","High","Active"),
  ("TC-NAV-006","Navigation","Upload direct URL","Upload page responds","Browser open","Navigate to /upload.html","Page loads","High","Active"),
  ("TC-NAV-007","Navigation","History direct URL","History page responds","Browser open","Navigate to /history.html","Page loads","High","Active"),
  ("TC-NAV-008","Navigation","Results direct URL","Results page responds","Browser open","Navigate to /results.html","Page loads","High","Active"),
  ("TC-NAV-009","Navigation","Viewer direct URL","Viewer page responds","Browser open","Navigate to /viewer.html","Page loads","High","Active"),
  ("TC-NAV-010","Navigation","Workflow direct URL","Workflow page responds","Browser open","Navigate to /workflow.html","Page loads","Medium","Active"),
  ("TC-NAV-011","Navigation","Refine direct URL","Refine page responds","Browser open","Navigate to /refine.html","Page loads","Medium","Active"),
  ("TC-NAV-012","Navigation","Signup link from login","Clicking signup navigates","Login page open","Click signup link","URL contains signup","High","Active"),
  ("TC-NAV-013","Navigation","Login link from signup","Clicking login navigates","Signup page open","Click login link","URL contains login","High","Active"),
  ("TC-NAV-014","Navigation","Browser back button","Back button works","Multiple pages visited","Click browser back","Page changes","Medium","Active"),
  ("TC-NAV-015","Navigation","Browser forward button","Forward button works","Multiple pages visited","Click back then forward","URL changes","Medium","Active"),
  ("TC-NAV-016","Navigation","Direct URL all pages","All page URLs respond","Browser open","Loop through PAGES dict","Each has title","High","Active"),
  ("TC-NAV-017","Navigation","404 page handling","Non-existent page handled","Browser open","Navigate to /nonexistent.html","No crash","Medium","Active"),
  ("TC-NAV-018","Navigation","Login URL is HTTPS","URL scheme correct","Browser open","Load login, check URL","https://","Critical","Active"),
  ("TC-NAV-019","Navigation","No mixed content","No HTTP on HTTPS page","Login page open","Check browser logs","No mixed content warnings","High","Active"),
  ("TC-NAV-020","Navigation","All pages return 200","HTTP status 200 for main pages","Browser open","XHR GET each page URL","Status = 200","High","Active"),
  ("TC-NAV-021","Navigation","Login URL contains domain","Correct domain in URL","Login page open","Inspect URL","github.io domain present","High","Active"),
  ("TC-NAV-022","Navigation","Pages load CSS","Stylesheet links present","Login page open","Count link[rel=stylesheet]","At least 1 CSS file","Medium","Active"),
  ("TC-NAV-023","Navigation","Pages load JS","Script tags present","Login page open","Count script[src]","JS files present","Medium","Active"),
  ("TC-NAV-024","Navigation","Meta viewport on login","Responsive meta tag","Login page open","Find meta[name=viewport]","Tag present","High","Active"),
  ("TC-NAV-025","Navigation","Meta viewport on signup","Responsive meta tag","Signup page open","Find meta[name=viewport]","Tag present","High","Active"),
  ("TC-NAV-026","Navigation","HTML5 doctype","Pages use HTML5","Login page open","Check source start","<!DOCTYPE html> present","Medium","Active"),
  ("TC-NAV-027","Navigation","Favicon present","Site has icon","Login page open","Check link[rel=icon]","Favicon link found","Low","Active"),
  ("TC-NAV-028","Navigation","UTF-8 charset declared","Character encoding set","Login page open","Check charset meta","utf-8 declared","Medium","Active"),
  ("TC-NAV-029","Navigation","No broken images","All images load","Login page open","Check naturalWidth of all img","naturalWidth > 0","Medium","Active"),
  ("TC-NAV-030","Navigation","All pages have titles","Document titles not empty","Login/signup/forgot open","Check driver.title","Title.length > 0 on each","High","Active"),
]
ALL_TESTS.extend(NAV)

# ═══════════════════════════════════════════════════════════════════════════════
# UPLOAD  (TC-UPLOAD-001 … 020)
# ═══════════════════════════════════════════════════════════════════════════════
UPLOAD = [
  ("TC-UPLOAD-001","File Upload","Upload page loads","Page loads successfully","Browser open","Navigate to /upload.html","Title not empty","Critical","Active"),
  ("TC-UPLOAD-002","File Upload","Upload page HTTPS","Page served over HTTPS","Browser open","Check URL scheme","https://","Critical","Active"),
  ("TC-UPLOAD-003","File Upload","No server error upload","No 500 on upload page","Upload page open","Inspect source","No 'Internal Server Error'","High","Active"),
  ("TC-UPLOAD-004","File Upload","File input present","input[type=file] exists","Upload page open","Inspect DOM","File input found","Critical","Active"),
  ("TC-UPLOAD-005","File Upload","Upload button present","Submit button visible","Upload page open","Inspect DOM","Upload button visible","Critical","Active"),
  ("TC-UPLOAD-006","File Upload","Upload button enabled","Button not disabled","Upload page open","Check button.isEnabled()","Enabled=True","High","Active"),
  ("TC-UPLOAD-007","File Upload","Drop zone or input","Drag-drop or file input","Upload page open","Check .drop-zone or file input","Either present","High","Active"),
  ("TC-UPLOAD-008","File Upload","Upload instructions","File type hints present","Upload page open","Inspect source","DICOM/zip/nifti mentioned","Medium","Active"),
  ("TC-UPLOAD-009","File Upload","CSS loaded on upload","Stylesheet present","Upload page open","Count CSS links","At least 1 CSS","Medium","Active"),
  ("TC-UPLOAD-010","File Upload","Upload loads under 5s","Performance check","Browser open","Time page load","< 5 seconds","High","Active"),
  ("TC-UPLOAD-011","File Upload","Upload mobile 320px","Mobile layout renders","320x568 viewport","Load upload page","File input or page loads","High","Active"),
  ("TC-UPLOAD-012","File Upload","No overflow mobile","No horizontal scroll","375x667 viewport","Check scrollWidth","scrollWidth <= viewportWidth","High","Active"),
  ("TC-UPLOAD-013","File Upload","Upload tablet 768px","Tablet layout renders","768x1024 viewport","Load upload page","File input present","Medium","Active"),
  ("TC-UPLOAD-014","File Upload","File input type=file","Correct input type","Upload page open","Check type attribute","type='file'","High","Active"),
  ("TC-UPLOAD-015","File Upload","Accept attribute string","Accept attribute valid","Upload page open","Check accept attribute","String (can be empty)","Medium","Active"),
  ("TC-UPLOAD-016","File Upload","Attach DICOM file","DICOM file accepted by input","Upload page open","send_keys DICOM path to input","files.length > 0","Critical","Active"),
  ("TC-UPLOAD-017","File Upload","Attach NIfTI file","NIfTI file accepted","Upload page open","send_keys .nii path","files.length > 0","Critical","Active"),
  ("TC-UPLOAD-018","File Upload","Attach ZIP file","ZIP file accepted","Upload page open","send_keys .zip path","files.length > 0","High","Active"),
  ("TC-UPLOAD-019","File Upload","Attach invalid extension","Non-medical file handled","Upload page open","send_keys .txt path","No crash","High","Active"),
  ("TC-UPLOAD-020","File Upload","XSS in upload not reflected","Filename XSS safe","Upload page open","send_keys file, submit","<script> not in source","Critical","Active"),
]
ALL_TESTS.extend(UPLOAD)

# ═══════════════════════════════════════════════════════════════════════════════
# HISTORY PAGE  (TC-HIST-001 … 020)
# ═══════════════════════════════════════════════════════════════════════════════
HISTORY = [
  ("TC-HIST-001","History","History page loads","Page loads without error","Browser open","Navigate to /history.html","Title not empty","Critical","Active"),
  ("TC-HIST-002","History","History page HTTPS","HTTPS enforced","Browser open","Check URL","https://","Critical","Active"),
  ("TC-HIST-003","History","No server error history","No 500 on history","History page open","Inspect source","No 'Internal Server Error'","High","Active"),
  ("TC-HIST-004","History","Page has content","Source not empty","History page open","Check len(source)","source > 200 chars","Medium","Active"),
  ("TC-HIST-005","History","Loads within 5s","Performance check","Browser open","Time page load","< 5 seconds","High","Active"),
  ("TC-HIST-006","History","CSS loaded","Stylesheet present","History page open","Count CSS links","At least 1 CSS","Medium","Active"),
  ("TC-HIST-007","History","Table or empty state","Content or empty state shown","History page open","Check table or empty div","Either visible","High","Active"),
  ("TC-HIST-008","History","Scan rows are elements","Rows are valid DOM elements","History page open","Count scan rows","Returns integer","Medium","Active"),
  ("TC-HIST-009","History","No patient data unauthed","Auth required for data","No session","Load history page","No patient_id in source","Critical","Active"),
  ("TC-HIST-010","History","No real data unauthed","No scan records without auth","No session","Load history page","Empty or login redirect","Critical","Active"),
  ("TC-HIST-011","History","Search input present","Search box available","History page open","Inspect search input","Search input found (soft)","High","Active"),
  ("TC-HIST-012","History","Search accepts input","Can type in search","History page open","type_text in search","Value reflects input","High","Active"),
  ("TC-HIST-013","History","Search clearable","Search can be cleared","History page open","Type then clear search","Value = ''","Medium","Active"),
  ("TC-HIST-014","History","Search XSS safe","XSS in search not reflected","History page open","Enter <script> in search","Not in page source","Critical","Active"),
  ("TC-HIST-015","History","Search SQL safe","SQLi in search handled","History page open","Enter OR 1=1 in search","No crash","Critical","Active"),
  ("TC-HIST-016","History","Filter control present","Filter visible (soft)","History page open","Check .filter-btn","Present or page loaded","Medium","Active"),
  ("TC-HIST-017","History","Sort controls present","Sort by column (soft)","History page open","Count sortable headers","Present or page loaded","Medium","Active"),
  ("TC-HIST-018","History","Pagination present","Pagination when rows > page","History page open","Check .pagination","Present if rows > 20","Medium","Active"),
  ("TC-HIST-019","History","History mobile 320px","Mobile layout renders","320x568 viewport","Load history page","Title not empty","High","Active"),
  ("TC-HIST-020","History","No overflow mobile","No horizontal scroll","375x667 viewport","Check scrollWidth","scrollWidth <= viewportWidth","High","Active"),
]
ALL_TESTS.extend(HISTORY)

# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE & RESET PASSWORD  (TC-PROF-001 … 020, TC-RESET-001 … 010)
# ═══════════════════════════════════════════════════════════════════════════════
PROFILE = [
  ("TC-PROF-001","Profile","Profile page loads","Page loads without error","Browser open","Navigate to /profile or /dashboard","Title not empty","Critical","Active"),
  ("TC-PROF-002","Profile","Profile HTTPS","Page served HTTPS","Browser open","Check URL scheme","https://","Critical","Active"),
  ("TC-PROF-003","Profile","No server error profile","No 500 on profile","Profile page open","Inspect source","No 500 error","High","Active"),
  ("TC-PROF-004","Profile","Profile has content","Source not empty","Profile page open","Check len(source)","source > 200","Medium","Active"),
  ("TC-PROF-005","Profile","Loads within 5s","Performance check","Browser open","Time load","< 5 seconds","High","Active"),
  ("TC-PROF-006","Profile","Name field visible","Name input present","Profile page open","Inspect input","Name field or page loads","High","Active"),
  ("TC-PROF-007","Profile","Email field present","Email input present","Profile page open","Inspect input","Email or page loads","High","Active"),
  ("TC-PROF-008","Profile","Save button present","Save button available","Profile page open","Inspect save button","Button present if form shown","High","Active"),
  ("TC-PROF-009","Profile","Change password section","Change pwd inputs present","Profile page open","Check pwd inputs","Section present (soft)","High","Active"),
  ("TC-PROF-010","Profile","No plaintext password","Password not in source","Profile page open","Inspect source","TestPass123! not in HTML","Critical","Active"),
  ("TC-PROF-011","Profile","Name field accepts input","Can type name","Profile page open","Type in name field","Value reflects input","High","Active"),
  ("TC-PROF-012","Profile","Phone field accepts input","Can type phone","Profile page open","Type in phone field","Value reflects input","Medium","Active"),
  ("TC-PROF-013","Profile","Clinic field accepts input","Can type clinic","Profile page open","Type in clinic field","Value reflects input","Medium","Active"),
  ("TC-PROF-014","Profile","XSS in name not reflected","Name XSS safe","Profile page open","Enter <script> in name","Not in source","Critical","Active"),
  ("TC-PROF-015","Profile","SQL in name handled","SQLi in name safe","Profile page open","Enter DROP TABLE in name","No crash","Critical","Active"),
  ("TC-PROF-016","Profile","Change pwd empty blocked","Empty current blocked","Profile page open","Submit empty current pwd","No password change","High","Active"),
  ("TC-PROF-017","Profile","Change pwd mismatch","Mismatch shown","Profile page open","Enter mismatched new pwds","Error or no change","High","Active"),
  ("TC-PROF-018","Profile","Change pwd weak rejected","Weak pwd rejected","Profile page open","Enter '123' as new pwd","Error or no change","High","Active"),
  ("TC-PROF-019","Profile","Credentials section renders","Cred section present","Profile page open","Check credential inputs","Section renders (soft)","Medium","Active"),
  ("TC-PROF-020","Profile","Credential type accepts input","Can type cred type","Profile page open","Type in cred type field","Value reflects input","Medium","Active"),
]
RESET = [
  ("TC-RESET-001","Reset Password","Reset page loads","Page loads","Browser open","Navigate to /reset-password.html","Title not empty","High","Active"),
  ("TC-RESET-002","Reset Password","Reset page HTTPS","HTTPS enforced","Browser open","Check URL","https://","Critical","Active"),
  ("TC-RESET-003","Reset Password","New pwd field visible","Input present","Reset page open","Inspect input","New pwd field visible","High","Active"),
  ("TC-RESET-004","Reset Password","Submit button visible","Button present","Reset page open","Inspect button","Submit button visible","High","Active"),
  ("TC-RESET-005","Reset Password","Empty submit stays","Empty form stays on page","Reset page open","Submit empty form","No crash or stays","High","Active"),
  ("TC-RESET-006","Reset Password","Weak password rejected","Min length enforced","Reset page open","Enter '123', submit","Error or no change","High","Active"),
  ("TC-RESET-007","Reset Password","Mismatched passwords","Mismatch detected","Reset page open","Enter different new/confirm","Error shown","High","Active"),
  ("TC-RESET-008","Reset Password","XSS in password safe","XSS not executed","Reset page open","Enter <script> in pwd","Not in source","Critical","Active"),
  ("TC-RESET-009","Reset Password","Invalid token handled","Bad token graceful","Reset page open","Append fake token to URL","No crash","High","Active"),
  ("TC-RESET-010","Reset Password","Has login link","Link back to login","Reset page open","Inspect login link","Link present (soft)","Medium","Active"),
]
ALL_TESTS.extend(PROFILE)
ALL_TESTS.extend(RESET)

# ═══════════════════════════════════════════════════════════════════════════════
# FORMS & INPUT VALIDATION  (TC-FORM-001 … 025, TC-INP-001 … 040)
# ═══════════════════════════════════════════════════════════════════════════════
FORMS = [
  ("TC-FORM-001","Forms","Login email clearable","Email field can be cleared","Login page open","Enter email, clear it","Value = ''","Medium","Active"),
  ("TC-FORM-002","Forms","Login password clearable","Password field clearable","Login page open","Enter pwd, clear it","Value = ''","Medium","Active"),
  ("TC-FORM-003","Forms","Login email max length","Long email handled","Login page open","Enter 200-char email","No crash","Medium","Active"),
  ("TC-FORM-004","Forms","Login whitespace-only email","Spaces only email blocked","Login page open","Enter spaces, submit","Stays on login","High","Active"),
  ("TC-FORM-005","Forms","Enter key submits login","Enter in pwd submits","Login page open","Type pwd, press Enter","Form submitted","High","Active"),
  ("TC-FORM-006","Forms","Signup all fields clearable","All signup fields clearable","Signup page open","Fill and clear all","Values = ''","Medium","Active"),
  ("TC-FORM-007","Forms","Signup name special chars","Hyphens and apostrophes","Signup page open","Enter O'Brien-Smith","Value stored","Medium","Active"),
  ("TC-FORM-008","Forms","Login email uppercase","Uppercase email accepted","Login page open","Enter DOCTOR@TEST.COM","Value not empty","Low","Active"),
  ("TC-FORM-009","Forms","Login password unicode","Unicode chars in password","Login page open","Enter Tëst123!","Value not empty","Medium","Active"),
  ("TC-FORM-010","Forms","Login email with plus","Plus sign in email","Login page open","Enter doc+test@test.com","Plus in value","Low","Active"),
  ("TC-FORM-011","Forms","Signup numbers-only pwd","Numeric password attempted","Signup page open","Enter 12345678","No crash","Medium","Active"),
  ("TC-FORM-012","Forms","Double-click submit","Double submit handled","Login page open","Fill form, double-click submit","No crash","Medium","Active"),
  ("TC-FORM-013","Forms","Tab traverses login fields","Tab key focuses next field","Login page open","Tab from email field","Next element focused","Medium","Active"),
  ("TC-FORM-014","Forms","License numeric input","License accepts numbers","Signup page open","Enter 123456","Value contains numbers","Low","Active"),
  ("TC-FORM-015","Forms","Email with subdomain","Subdomain email accepted","Login page open","Enter user@clinic.hospital.com","Value not empty","Low","Active"),
  ("TC-FORM-016","Forms","Forgot pwd submit visible","Submit button present","Forgot pwd page open","Inspect DOM","Submit button visible","High","Active"),
  ("TC-FORM-017","Forms","Forgot pwd email visible","Email field visible","Forgot pwd page open","Inspect DOM","Email field visible","High","Active"),
  ("TC-FORM-018","Forms","Login form no HTTP action","Form not posting to HTTP","Login page open","Check form action","Not http://","High","Active"),
  ("TC-FORM-019","Forms","Signup form present","Form element exists","Signup page open","Inspect DOM","Form found","High","Active"),
  ("TC-FORM-020","Forms","Upload file input present","File input in upload form","Upload page open","Inspect DOM","File input found","Critical","Active"),
  ("TC-FORM-021","Forms","Empty login no 500","Empty submit no server error","Login page open","Click login empty","No 500 error","High","Active"),
  ("TC-FORM-022","Forms","Empty signup no 500","Empty submit no server error","Signup page open","Click signup empty","No 500 error","High","Active"),
  ("TC-FORM-023","Forms","Email with IP domain","IP address domain handled","Login page open","Enter user@192.168.1.1","Value not empty","Low","Active"),
  ("TC-FORM-024","Forms","Password with spaces","Password with spaces accepted","Login page open","Enter 'Test 123 !'","Value not empty","Low","Active"),
  ("TC-FORM-025","Forms","Form fields labeled","Email has label or placeholder","Login page open","Check aria-label or placeholder","Accessibility present","High","Active"),
]
INP = [
  ("TC-INP-001","Input Validation","SQL injection OR bypass","OR 1=1 email rejected","Login page open","Enter ' OR '1'='1 in email","Stays on login","Critical","Active"),
  ("TC-INP-002","Input Validation","SQL injection comment","Comment bypass rejected","Login page open","Enter admin'-- in email","Stays on login","Critical","Active"),
  ("TC-INP-003","Input Validation","SQL UNION injection","UNION SELECT rejected","Login page open","Enter UNION SELECT in email","Stays on login","Critical","Active"),
  ("TC-INP-004","Input Validation","SQL DROP TABLE","DROP TABLE rejected","Login page open","Enter DROP TABLE in email","Stays on login","Critical","Active"),
  ("TC-INP-005","Input Validation","XSS script tag email","Script tag not executed","Login page open","Enter <script>alert in email","XSS not in source","Critical","Active"),
  ("TC-INP-006","Input Validation","XSS img onerror","img onerror not executed","Login page open","Enter img onerror payload","No crash","Critical","Active"),
  ("TC-INP-007","Input Validation","XSS javascript: protocol","javascript: protocol safe","Login page open","Enter javascript:alert","No crash","Critical","Active"),
  ("TC-INP-008","Input Validation","Empty email blocked","Empty email handled","Login page open","Submit empty email","Stays on login","High","Active"),
  ("TC-INP-009","Input Validation","Empty password blocked","Empty password handled","Login page open","Submit empty password","Stays on login","High","Active"),
  ("TC-INP-010","Input Validation","Whitespace email blocked","Whitespace email rejected","Login page open","Submit '   ' email","Stays on login","High","Active"),
  ("TC-INP-011","Input Validation","500-char email handled","Very long email safe","Login page open","Enter 500-char email","No crash","Medium","Active"),
  ("TC-INP-012","Input Validation","1000-char password safe","Very long password safe","Login page open","Enter 1000-char password","No crash","Medium","Active"),
  ("TC-INP-013","Input Validation","Null bytes in email","Null byte handled","Login page open","Enter null byte in email","No crash","High","Active"),
  ("TC-INP-014","Input Validation","Special chars in email","Special chars handled","Login page open","Enter !#$%&' in email","No crash","Medium","Active"),
  ("TC-INP-015","Input Validation","HTML entities in email","HTML entities safe","Login page open","Enter &lt;test&gt; in email","No crash","Medium","Active"),
  ("TC-INP-016","Input Validation","Newline in email","Newline safe","Login page open","Enter \\n in email","No crash","High","Active"),
  ("TC-INP-017","Input Validation","Tab in email","Tab char safe","Login page open","Enter \\t in email","No crash","Medium","Active"),
  ("TC-INP-018","Input Validation","Unicode email","Unicode chars handled","Login page open","Enter tëst@ëxample.com","No crash","Medium","Active"),
  ("TC-INP-019","Input Validation","Emoji in password","Emoji in password safe","Login page open","Enter Test123!😀","No crash","Low","Active"),
  ("TC-INP-020","Input Validation","CRLF injection email","CRLF safe","Login page open","Enter \\r\\n in email","No crash","High","Active"),
  ("TC-INP-021","Input Validation","Name boundary min (2 chars)","Min length works","Signup page open","Enter 2-char name","No crash","Medium","Active"),
  ("TC-INP-022","Input Validation","Name boundary max (100 chars)","Max length works","Signup page open","Enter 100-char name","No crash","Medium","Active"),
  ("TC-INP-023","Input Validation","Name over max (101 chars)","Over max handled","Signup page open","Enter 101-char name","No crash or error","Medium","Active"),
  ("TC-INP-024","Input Validation","Password min valid (8 chars)","Min password works","Signup page open","Enter 8-char password","No crash","High","Active"),
  ("TC-INP-025","Input Validation","Password too short (5 chars)","Short password rejected","Signup page open","Enter 5-char password","Error or blocked","High","Active"),
  ("TC-INP-026","Input Validation","Numeric-only name","Numbers in name","Signup page open","Enter '12345'","No crash","Low","Active"),
  ("TC-INP-027","Input Validation","Email missing @ sign","No @ rejected","Login page open","Enter 'usernameonly'","Stays on login","High","Active"),
  ("TC-INP-028","Input Validation","Email missing domain","No domain rejected","Login page open","Enter 'user@'","Stays on login","High","Active"),
  ("TC-INP-029","Input Validation","Email double @ sign","Double @ rejected","Login page open","Enter 'user@@domain.com'","Stays on login","High","Active"),
  ("TC-INP-030","Input Validation","Numeric-only email local","Numbers in local part","Login page open","Enter '123456@test.com'","No crash","Low","Active"),
  ("TC-INP-031","Input Validation","Password all spaces","Spaces password safe","Login page open","Enter 8 spaces as password","No crash","Medium","Active"),
  ("TC-INP-032","Input Validation","Script tag in signup name","XSS in name not stored","Signup page open","Enter <script>cookie in name","Not in source","Critical","Active"),
  ("TC-INP-033","Input Validation","SQL in signup name","SQLi in name handled","Signup page open","Enter DROP TABLE in name","No crash","Critical","Active"),
  ("TC-INP-034","Input Validation","SQL in forgot pwd email","SQLi in forgot pwd safe","Forgot pwd page open","Enter OR 1=1 in email","No crash","Critical","Active"),
  ("TC-INP-035","Input Validation","XSS in forgot pwd email","XSS in forgot pwd safe","Forgot pwd page open","Enter <script> in email","Not in source","Critical","Active"),
  ("TC-INP-036","Input Validation","SQL in license field","SQLi in license safe","Signup page open","Enter DROP TABLE in license","No crash","Critical","Active"),
  ("TC-INP-037","Input Validation","Path traversal in email","../etc/passwd safe","Login page open","Enter ../../etc/passwd@test.com","No crash","High","Active"),
  ("TC-INP-038","Input Validation","SQL in password field","SQLi in password safe","Login page open","Enter ' OR '1'='1 as pwd","No crash","Critical","Active"),
  ("TC-INP-039","Input Validation","Null-encoded email","URL-encoded null safe","Login page open","Enter %00admin%00@test.com","No crash","High","Active"),
  ("TC-INP-040","Input Validation","Overlong name 500 chars","500-char name handled","Signup page open","Enter 500-char name","No crash","Medium","Active"),
]
ALL_TESTS.extend(FORMS)
ALL_TESTS.extend(INP)

# ═══════════════════════════════════════════════════════════════════════════════
# ACCESSIBILITY  (TC-ACC-001 … 020)
# ═══════════════════════════════════════════════════════════════════════════════
ACC = [
  ("TC-ACC-001","Accessibility","Login email has label","Email labeled for screen readers","Login page open","Check aria-label or label","Label or placeholder present","High","Active"),
  ("TC-ACC-002","Accessibility","Login password has label","Password labeled","Login page open","Check aria-label or label","Label or placeholder present","High","Active"),
  ("TC-ACC-003","Accessibility","Images have alt text","All img elements have alt","Login page open","Check all img.alt","alt not None","High","Active"),
  ("TC-ACC-004","Accessibility","Buttons have text","Buttons are accessible","Login page open","Check button text/aria-label","Each button has text","High","Active"),
  ("TC-ACC-005","Accessibility","Main landmark present","<main> or role=main","Login page open","Check DOM","main element present (soft)","Medium","Active"),
  ("TC-ACC-006","Accessibility","Links have href","All anchors have href","Login page open","Check all a[href]","href not empty","High","Active"),
  ("TC-ACC-007","Accessibility","Email input type=email","Correct type for keyboard","Login page open","Check type attribute","type in (email, text)","High","Active"),
  ("TC-ACC-008","Accessibility","Form has submit button","Form submittable by keyboard","Login page open","Count button[type=submit]","At least 1 submit","High","Active"),
  ("TC-ACC-009","Accessibility","HTML lang attribute","Language declared","Login page open","Check html.lang","lang not None","High","Active"),
  ("TC-ACC-010","Accessibility","No positive tabindex","Tab order not broken","Login page open","Check [tabindex]","No tabindex > 0","High","Active"),
  ("TC-ACC-011","Accessibility","Skip navigation link","Skip-nav for keyboard users","Login page open","Check .skip-nav","Present (soft)","Medium","Active"),
  ("TC-ACC-012","Accessibility","Error messages descriptive","Error messages meaningful","Login page open","Submit empty, check error","Message > 2 chars or none","High","Active"),
  ("TC-ACC-013","Accessibility","Login keyboard accessible","Tab focuses each field","Login page open","Tab through form","Focus moves correctly","High","Active"),
  ("TC-ACC-014","Accessibility","Heading hierarchy","h1 before h2","Login page open","Count h1 elements","Headings ordered","Medium","Active"),
  ("TC-ACC-015","Accessibility","No blink/marquee","No accessibility-breaking elements","Login page open","Check blink/marquee","None present","Medium","Active"),
  ("TC-ACC-016","Accessibility","Focus visible on input","Focus indicator present","Login page open","Click email, check outline","Outline not None","High","Active"),
  ("TC-ACC-017","Accessibility","Buttons not divs","Semantic button elements","Login page open","Check div[onclick]","No div-buttons (soft)","Medium","Active"),
  ("TC-ACC-018","Accessibility","Signup inputs labeled","All signup inputs accessible","Signup page open","Check each input for label","Label or placeholder","High","Active"),
  ("TC-ACC-019","Accessibility","Signup HTML lang","Language declared on signup","Signup page open","Check html.lang","lang not None","High","Active"),
  ("TC-ACC-020","Accessibility","Viewport zoom not blocked","User zoom not disabled","Login page open","Check meta viewport content","user-scalable=no absent","High","Active"),
]
ALL_TESTS.extend(ACC)

# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSIVE  (TC-RESP-001 … 020)
# ═══════════════════════════════════════════════════════════════════════════════
RESP = [
  ("TC-RESP-001","Responsive","Login 320px renders","320px mobile layout","320x568","Load login page","Email field visible","High","Active"),
  ("TC-RESP-002","Responsive","Login 375px renders","375px mobile layout","375x667","Load login page","Login button visible","High","Active"),
  ("TC-RESP-003","Responsive","Login 768px renders","Tablet layout","768x1024","Load login page","Email field visible","High","Active"),
  ("TC-RESP-004","Responsive","Login 1280px renders","Laptop layout","1280x800","Load login page","Email field visible","High","Active"),
  ("TC-RESP-005","Responsive","Login 1920px renders","Desktop layout","1920x1080","Load login page","Email field visible","Medium","Active"),
  ("TC-RESP-006","Responsive","Signup 320px renders","320px mobile layout","320x568","Load signup page","Email visible","High","Active"),
  ("TC-RESP-007","Responsive","Signup 768px renders","Tablet layout","768x1024","Load signup page","All fields visible","High","Active"),
  ("TC-RESP-008","Responsive","No overflow at 320px","No horizontal scroll","320x568","Check scrollWidth","scrollWidth <= vw","High","Active"),
  ("TC-RESP-009","Responsive","No overflow at 375px","No horizontal scroll","375x667","Check scrollWidth","scrollWidth <= vw","High","Active"),
  ("TC-RESP-010","Responsive","No overflow at 768px","No horizontal scroll","768x1024","Check scrollWidth","scrollWidth <= vw","High","Active"),
  ("TC-RESP-011","Responsive","Meta viewport exists","Responsive meta tag","Login page open","Count meta[name=viewport]","At least 1","Critical","Active"),
  ("TC-RESP-012","Responsive","Touch target large enough","Buttons ≥ 44px tall","375x667","Measure login button height","height >= 30px","High","Active"),
  ("TC-RESP-013","Responsive","Text readable mobile","Font >= 14px on mobile","375x667","Check computed font-size","fontSize >= 12","High","Active"),
  ("TC-RESP-014","Responsive","Upload page 320px","Upload mobile layout","320x568","Load upload page","Page loads","High","Active"),
  ("TC-RESP-015","Responsive","History page 320px","History mobile layout","320x568","Load history page","Page loads","High","Active"),
  ("TC-RESP-016","Responsive","Forgot pwd 320px","Forgot pwd mobile","320x568","Load forgot pwd page","Email visible","High","Active"),
  ("TC-RESP-017","Responsive","Signup no overflow mobile","No overflow at 375px","375x667","Check scrollWidth on signup","scrollWidth <= vw+10","High","Active"),
  ("TC-RESP-018","Responsive","All public pages 320px","All pages mobile-safe","320x568","Load login/signup/forgot","Each has title","High","Active"),
  ("TC-RESP-019","Responsive","Portrait to landscape","Orientation change handled","Login page open","Resize 375x667 then 667x375","Email visible both ways","Medium","Active"),
  ("TC-RESP-020","Responsive","2560x1440 no overflow","4K no overflow","2560x1440","Load login, check scrollWidth","scrollWidth <= vw","Medium","Active"),
]
ALL_TESTS.extend(RESP)

# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE SMOKE  (TC-PERF-001 … 020)
# ═══════════════════════════════════════════════════════════════════════════════
PERF = [
  ("TC-PERF-001","Performance","Login loads under 5s","Page load time","Browser open","Time login page load","< 5 seconds","High","Active"),
  ("TC-PERF-002","Performance","Signup loads under 5s","Page load time","Browser open","Time signup page load","< 5 seconds","High","Active"),
  ("TC-PERF-003","Performance","Forgot pwd loads under 5s","Page load time","Browser open","Time forgot pwd load","< 5 seconds","High","Active"),
  ("TC-PERF-004","Performance","Dashboard loads under 5s","Page load time","Browser open","Time dashboard load","< 5 seconds","High","Active"),
  ("TC-PERF-005","Performance","Upload page loads under 5s","Page load time","Browser open","Time upload page load","< 5 seconds","High","Active"),
  ("TC-PERF-006","Performance","DOM content loaded under 3s","DOM load timing","Login page open","performance.timing","domContentLoaded < 3000ms","High","Active"),
  ("TC-PERF-007","Performance","Signup DOM load under 3s","DOM load timing","Signup page open","performance.timing","domContentLoaded < 3000ms","High","Active"),
  ("TC-PERF-008","Performance","Resource count login","Reasonable resource count","Login page open","Count resources","< 100 resources","Medium","Active"),
  ("TC-PERF-009","Performance","No large inline scripts","Inline script size","Login page open","Check inline script length","Each < 512KB","Medium","Active"),
  ("TC-PERF-010","Performance","First Contentful Paint","FCP metric check","Login page open","Get FCP timing","FCP < 5000ms or -1","High","Active"),
  ("TC-PERF-011","Performance","Page weight reasonable","Total transfer size","Login page open","Sum resource transferSize","< 10MB","High","Active"),
  ("TC-PERF-012","Performance","Login fully loaded under 3s","Full load timing","Login page open","loadEventEnd - navigationStart","< 3000ms","High","Active"),
  ("TC-PERF-013","Performance","Signup fully loaded under 3s","Full load timing","Signup page open","loadEventEnd - navigationStart","< 3000ms","High","Active"),
  ("TC-PERF-014","Performance","Rapid navigation under 15s","Multi-page navigation","Browser open","Navigate 3 pages in sequence","Total < 15 seconds","Medium","Active"),
  ("TC-PERF-015","Performance","Repeat load is cached","Cache improves load","Login page open x2","Compare load times","Second load ≤ 2x first","Medium","Active"),
  ("TC-PERF-016","Performance","CSS loaded under 2s","CSS resource timing","Login page open","Check CSS resource durations","Each < 2000ms","Medium","Active"),
  ("TC-PERF-017","Performance","JS loaded under 2s","JS resource timing","Login page open","Check script resource durations","Each < 2000ms","Medium","Active"),
  ("TC-PERF-018","Performance","performance API available","Browser performance API","Login page open","Check typeof window.performance","'object'","Low","Active"),
  ("TC-PERF-019","Performance","No excessive render-blocking","Render-blocking check","Login page open","Check renderBlockingStatus","<= 5 blocking resources","Medium","Active"),
  ("TC-PERF-020","Performance","Page under 2MB total","Total page size","Login page open","Sum decodedBodySize","< 2,000,000 bytes","High","Active"),
]
ALL_TESTS.extend(PERF)

# ═══════════════════════════════════════════════════════════════════════════════
# UI VALIDATION  (TC-UI-001 … 050)
# ═══════════════════════════════════════════════════════════════════════════════
UI = [
  ("TC-UI-001","UI Validation","Login has brand logo","Brand visible on login","Login page open","Check .logo or h1","Brand element present","High","Active"),
  ("TC-UI-002","UI Validation","Login layout 1920px","Desktop layout correct","1920x1080","Load login page","Email + button visible","High","Active"),
  ("TC-UI-003","UI Validation","Login layout 768px","Tablet layout correct","768x1024","Load login page","Fields visible","High","Active"),
  ("TC-UI-004","UI Validation","Login layout 375px","Mobile layout correct","375x667","Load login page","Email visible","High","Active"),
  ("TC-UI-005","UI Validation","Login button enabled","Button not disabled","Login page open","Check isEnabled()","True","High","Active"),
  ("TC-UI-006","UI Validation","Signup button enabled","Button not disabled","Signup page open","Check isEnabled()","True","High","Active"),
  ("TC-UI-007","UI Validation","Email input editable","Can type in email","Login page open","Type email","Value updated","High","Active"),
  ("TC-UI-008","UI Validation","Password input editable","Can type password","Login page open","Type password","Value not empty","High","Active"),
  ("TC-UI-009","UI Validation","Login body has background","Body has styling","Login page open","Inspect body element","body not None","Medium","Active"),
  ("TC-UI-010","UI Validation","Login form positioned","Form has width","Login page open","Get form bounding rect","width > 50px","High","Active"),
  ("TC-UI-011","UI Validation","Email placeholder or label","Email field labeled","Login page open","Check placeholder/aria-label","Not empty or label exists","High","Active"),
  ("TC-UI-012","UI Validation","Signup name visible","Name field shown","Signup page open","Check NAME_INPUT visibility","Visible","High","Active"),
  ("TC-UI-013","UI Validation","Signup license visible","License field shown","Signup page open","Check LICENSE_INPUT visibility","Visible","High","Active"),
  ("TC-UI-014","UI Validation","Signup email visible","Email field shown","Signup page open","Check EMAIL_INPUT visibility","Visible","High","Active"),
  ("TC-UI-015","UI Validation","Signup password visible","Password field shown","Signup page open","Check PASSWORD_INPUT visibility","Visible","High","Active"),
  ("TC-UI-016","UI Validation","Background not transparent","Page has visible background","Login page open","Check body backgroundColor","Not empty string","Medium","Active"),
  ("TC-UI-017","UI Validation","Font family defined","Page uses defined font","Login page open","Check body fontFamily","Not empty","Medium","Active"),
  ("TC-UI-018","UI Validation","No overflow at 375px","No horizontal scroll","375x667","Check scrollWidth on login","scrollWidth <= vw+20","High","Active"),
  ("TC-UI-019","UI Validation","Signup no overflow 375px","No horizontal scroll","375x667","Check scrollWidth on signup","scrollWidth <= vw+20","High","Active"),
  ("TC-UI-020","UI Validation","Login button has text","Button labeled","Login page open","Check button.text","Length > 0","High","Active"),
  ("TC-UI-021","UI Validation","Dashboard renders","Dashboard has content","Browser open","Load dashboard","source > 200 chars","High","Active"),
  ("TC-UI-022","UI Validation","Upload page renders","Upload has content","Browser open","Load upload","source > 200 chars","High","Active"),
  ("TC-UI-023","UI Validation","History page renders","History has content","Browser open","Load history","source > 200 chars","High","Active"),
  ("TC-UI-024","UI Validation","Results page renders","Results has content","Browser open","Load results","source > 200 chars","High","Active"),
  ("TC-UI-025","UI Validation","Viewer page renders","Viewer has content","Browser open","Load viewer","source > 200 chars","High","Active"),
  ("TC-UI-026","UI Validation","Login CSS loaded","Computed display set","Login page open","Check body display","Not 'none'","Medium","Active"),
  ("TC-UI-027","UI Validation","No lorem ipsum text","No placeholder text","Login page open","Search source","'lorem ipsum' absent","Medium","Active"),
  ("TC-UI-028","UI Validation","No TODO comments in HTML","No dev comments","Login page open","Search source","No <!-- TODO or FIXME","Medium","Active"),
  ("TC-UI-029","UI Validation","Login HTML lang attribute","Lang declared","Login page open","Check html.lang","Not None","High","Active"),
  ("TC-UI-030","UI Validation","Signup HTML lang attribute","Lang declared","Signup page open","Check html.lang","Not None","High","Active"),
  ("TC-UI-031","UI Validation","Email input type correct","Correct type attribute","Login page open","Check type attr","'email' or 'text'","High","Active"),
  ("TC-UI-032","UI Validation","Login has heading","Heading element present","Login page open","Count h1/h2/h3","At least 0 (soft)","Medium","Active"),
  ("TC-UI-033","UI Validation","Workflow page renders","Workflow has content","Browser open","Load workflow","source > 200","Medium","Active"),
  ("TC-UI-034","UI Validation","Refine page renders","Refine has content","Browser open","Load refine","source > 200","Medium","Active"),
  ("TC-UI-035","UI Validation","Login 2560px renders","4K layout","2560x1440","Load login","Email field visible","Medium","Active"),
  ("TC-UI-036","UI Validation","Images have alt text","Alt attribute on all imgs","Login page open","Check all img.alt","alt present","High","Active"),
  ("TC-UI-037","UI Validation","Login button type=submit","Correct button type","Login page open","Check button type","'submit' or 'button'","High","Active"),
  ("TC-UI-038","UI Validation","Signup button type","Correct button type","Signup page open","Check button type","'submit' or 'button'","High","Active"),
  ("TC-UI-039","UI Validation","Form required fields","Required attribute","Login page open","Check email required","Attribute present or visible","High","Active"),
  ("TC-UI-040","UI Validation","Color contrast check","Text not same as background","Login page open","Compare color vs backgroundColor","Not equal","High","Active"),
  ("TC-UI-041","UI Validation","Login has CSS files","At least 1 CSS loaded","Login page open","Count CSS link elements","Count >= 1","Medium","Active"),
  ("TC-UI-042","UI Validation","No duplicate IDs","Unique IDs in DOM","Login page open","Find duplicate IDs via JS","List is empty","High","Active"),
  ("TC-UI-043","UI Validation","Input fields focusable","Can click and focus","Login page open","Click email, check activeElement","TAG = INPUT","High","Active"),
  ("TC-UI-044","UI Validation","Tab moves focus","Focus moves on tab","Login page open","Tab from email","Next element focused","High","Active"),
  ("TC-UI-045","UI Validation","Page min height","Page is visible size","Login page open","Check body scrollHeight","> 300px","Medium","Active"),
  ("TC-UI-046","UI Validation","No overflow-x scroll","Body overflow-x","Login page open","Check overflowX","Not 'scroll'","High","Active"),
  ("TC-UI-047","UI Validation","Signup inputs styled","Border defined on inputs","Signup page open","Check borderWidth","Not None","Medium","Active"),
  ("TC-UI-048","UI Validation","Login font readable","Min font size","Login page open","Check body fontSize",">= 12px","High","Active"),
  ("TC-UI-049","UI Validation","Upload has file input","File input on upload","Upload page open","Check input[type=file]","Present","Critical","Active"),
  ("TC-UI-050","UI Validation","Pages use modern CSS","Flex or grid present","Login page open","Search source for flex/grid","Present (soft)","Low","Active"),
]
ALL_TESTS.extend(UI)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION MANAGEMENT  (TC-SESS-001 … 020)
# ═══════════════════════════════════════════════════════════════════════════════
SESS = [
  ("TC-SESS-001","Session","No stale cookie on login","No auth cookie fresh load","Browser open","Load login page","No session/auth cookies","High","Active"),
  ("TC-SESS-002","Session","No auth in localStorage","LocalStorage clean","Browser open","Load login, check localStorage","No token keys","High","Active"),
  ("TC-SESS-003","Session","No auth in sessionStorage","SessionStorage clean","Browser open","Load login, check sessionStorage","List is array","Medium","Active"),
  ("TC-SESS-004","Session","Refresh clears form","Form cleared on refresh","Login page open","Type email, refresh","Value empty after refresh","High","Active"),
  ("TC-SESS-005","Session","Back to login from signup","Navigation works","Signup then login","Navigate back","Login page loads","Medium","Active"),
  ("TC-SESS-006","Session","No auto-login on revisit","No automatic login","Browser open","Load login page","Not on dashboard","High","Active"),
  ("TC-SESS-007","Session","Minimal cookies set","Few cookies only","Login page open","Count cookies","Count <= 10","Medium","Active"),
  ("TC-SESS-008","Session","localStorage API works","Storage available","Login page open","Set and get item","Value matches","Low","Active"),
  ("TC-SESS-009","Session","sessionStorage API works","Storage available","Login page open","Set and get item","Value matches","Low","Active"),
  ("TC-SESS-010","Session","No token in URL","Credentials not in URL","Login page open","Check URL","No 'token=' in URL","Critical","Active"),
  ("TC-SESS-011","Session","Signup URL clean","No token on signup URL","Signup page open","Check URL","No 'token=' in URL","High","Active"),
  ("TC-SESS-012","Session","Forgot pwd URL clean","No token in URL","Forgot pwd page open","Check URL","No 'token=' in URL","High","Active"),
  ("TC-SESS-013","Session","Clear cookies and reload","Clearing cookies works","Login page open","Delete all cookies, reload","Login form still visible","High","Active"),
  ("TC-SESS-014","Session","Multiple tabs login","Login works in two tabs","Browser open","Open login in two tabs","Both load correctly","Medium","Active"),
  ("TC-SESS-015","Session","X-Frame-Options","Page not embeddable","Login page open","Load page","Page loads (header check elsewhere)","High","Active"),
  ("TC-SESS-016","Session","Fetch API available","Modern JS available","Login page open","typeof fetch","'function'","Medium","Active"),
  ("TC-SESS-017","Session","Signup submit triggers response","Form responds","Signup page open","Submit form","Response received","High","Active"),
  ("TC-SESS-018","Session","Login submit triggers response","Form responds","Login page open","Submit form","Response received","High","Active"),
  ("TC-SESS-019","Session","Password not in localStorage","Password not persisted","Login page open","Submit, check localStorage","TestPass123! absent","Critical","Active"),
  ("TC-SESS-020","Session","Password not in sessionStorage","Password not in session","Login page open","Submit, check sessionStorage","TestPass123! absent","Critical","Active"),
]
ALL_TESTS.extend(SESS)

# ═══════════════════════════════════════════════════════════════════════════════
# REGRESSION  (TC-REG-001 … 050)
# ═══════════════════════════════════════════════════════════════════════════════
REG = [
  ("TC-REG-001","Regression","Login page still works","Regression: login loads","Browser open","Load login page","Email + pwd + btn visible","Critical","Active"),
  ("TC-REG-002","Regression","Signup page still works","Regression: signup loads","Browser open","Load signup page","All fields visible","Critical","Active"),
  ("TC-REG-003","Regression","Forgot pwd still works","Regression: forgot pwd","Browser open","Load forgot pwd","Email field visible","High","Active"),
  ("TC-REG-004","Regression","Login to signup nav","Regression: navigation","Login page open","Click signup link","Navigates to signup","High","Active"),
  ("TC-REG-005","Regression","Signup to login nav","Regression: navigation","Signup page open","Click login link","Navigates to login","High","Active"),
  ("TC-REG-006","Regression","All pages have titles","Regression: titles","Browser open","Load 3 pages","Each has title","High","Active"),
  ("TC-REG-007","Regression","Page sources not empty","Regression: content","Browser open","Load 3 pages","Each source > 100 chars","High","Active"),
  ("TC-REG-008","Regression","No 404 on main pages","Regression: no 404","Browser open","Load login and signup","No '404 not found' in body","High","Active"),
  ("TC-REG-009","Regression","Login email accepts input","Regression: input works","Login page open","Type email","Value contains typed text","High","Active"),
  ("TC-REG-010","Regression","Login password accepts input","Regression: input works","Login page open","Type password","Value not empty","High","Active"),
  ("TC-REG-011","Regression","Signup name accepts input","Regression: input works","Signup page open","Type name","Value contains text","High","Active"),
  ("TC-REG-012","Regression","Signup email accepts input","Regression: input works","Signup page open","Type email","Value contains text","High","Active"),
  ("TC-REG-013","Regression","Buttons are clickable","Regression: interactivity","Login page open","Check button.isEnabled()","Enabled=True","High","Active"),
  ("TC-REG-014","Regression","Password masking preserved","Regression: security","Login page open","Check input type","type='password'","Critical","Active"),
  ("TC-REG-015","Regression","Login CSS loaded","Regression: styling","Login page open","Count CSS links",">= 1","Medium","Active"),
  ("TC-REG-016","Regression","Signup CSS loaded","Regression: styling","Signup page open","Count CSS links",">= 1","Medium","Active"),
  ("TC-REG-017","Regression","All pages still HTTPS","Regression: security","Browser open","Load 3 pages","All https://","Critical","Active"),
  ("TC-REG-018","Regression","No broken assets","Regression: resources","Login page open","Check resource load","< 5 zero-duration resources","Medium","Active"),
  ("TC-REG-019","Regression","Login form responds","Regression: form function","Login page open","Submit form","Response received","High","Active"),
  ("TC-REG-020","Regression","Signup form responds","Regression: form function","Signup page open","Submit form","Response received","High","Active"),
  ("TC-REG-021","Regression","Forgot pwd form responds","Regression: form function","Forgot pwd page open","Submit form","Response received","High","Active"),
  ("TC-REG-022","Regression","Login page refresh works","Regression: reload","Login page open","Refresh page","Form still visible","High","Active"),
  ("TC-REG-023","Regression","Signup page refresh works","Regression: reload","Signup page open","Refresh page","All fields visible","High","Active"),
  ("TC-REG-024","Regression","JS executes on login","Regression: JavaScript","Login page open","Execute 1+1","Result = 2","High","Active"),
  ("TC-REG-025","Regression","JS available (vanilla)","Regression: JavaScript","Login page open","Check querySelector","True","High","Active"),
  ("TC-REG-026","Regression","JS executes on signup","Regression: JavaScript","Signup page open","Execute 2*3","Result = 6","High","Active"),
  ("TC-REG-027","Regression","All input IDs unique","Regression: HTML quality","Login page open","Check for duplicate IDs","No duplicates","High","Active"),
  ("TC-REG-028","Regression","Body element present","Regression: HTML structure","Login and signup open","Count body elements","1 body each","High","Active"),
  ("TC-REG-029","Regression","Head element present","Regression: HTML structure","Login page open","Count head elements","1 head element","Medium","Active"),
  ("TC-REG-030","Regression","Title consistent on reload","Regression: consistency","Login page open","Get title before/after reload","Titles match","High","Active"),
  ("TC-REG-031","Regression","Upload page renders","Regression: page renders","Browser open","Load upload page","source > 200","High","Active"),
  ("TC-REG-032","Regression","History page renders","Regression: page renders","Browser open","Load history page","source > 200","High","Active"),
  ("TC-REG-033","Regression","Results page renders","Regression: page renders","Browser open","Load results page","source > 200","High","Active"),
  ("TC-REG-034","Regression","Viewer page renders","Regression: page renders","Browser open","Load viewer page","source > 200","High","Active"),
  ("TC-REG-035","Regression","Workflow page renders","Regression: page renders","Browser open","Load workflow page","source > 200","Medium","Active"),
  ("TC-REG-036","Regression","No lorem ipsum any page","Regression: content","Browser open","Load 3 pages","No 'lorem ipsum'","Medium","Active"),
  ("TC-REG-037","Regression","Links navigate correctly","Regression: links","Login page open","Check first 5 link hrefs","All https://","Medium","Active"),
  ("TC-REG-038","Regression","Page title not default","Regression: title","Login page open","Check title value","Not 'Document' or 'Untitled'","High","Active"),
  ("TC-REG-039","Regression","Form fields not hidden","Regression: visibility","Login page open","Check email isDisplayed()","True","High","Active"),
  ("TC-REG-040","Regression","All public pages under 5s","Regression: performance","Browser open","Time 3 page loads","Each < 5 seconds","High","Active"),
  ("TC-REG-041","Regression","Deploy URL accessible","Regression: deployment","Browser open","Load BASE_URL","Page loads","Critical","Active"),
  ("TC-REG-042","Regression","Login page HTTPS","Regression: HTTPS","Browser open","Load login, check URL","https://","Critical","Active"),
  ("TC-REG-043","Regression","No console errors login","Regression: clean console","Login page open","Check browser logs","0 SEVERE errors","High","Active"),
  ("TC-REG-044","Regression","No console errors signup","Regression: clean console","Signup page open","Check browser logs","0 SEVERE errors","High","Active"),
  ("TC-REG-045","Regression","Signup button has text","Regression: button label","Signup page open","Check button text","Length > 0","Medium","Active"),
  ("TC-REG-046","Regression","Login button has text","Regression: button label","Login page open","Check button text","Length > 0","Medium","Active"),
  ("TC-REG-047","Regression","JS not blocked","Regression: readyState","Login page open","Check readyState","'complete'","High","Active"),
  ("TC-REG-048","Regression","No mixed content signup","Regression: security","Signup page open","Check browser logs","No mixed content","High","Active"),
  ("TC-REG-049","Regression","Login readyState complete","Regression: page load","Login page open","Check readyState","'complete'","High","Active"),
  ("TC-REG-050","Regression","All 10 pages accessible","Smoke regression","Browser open","Load all 10 page URLs","Each has title","Critical","Active"),
]
ALL_TESTS.extend(REG)

print(f"Total test cases compiled: {len(ALL_TESTS)}")

# ─────────────────────────────────────────────────────────────────────────────
# BUILD THE EXCEL WORKBOOK
# ─────────────────────────────────────────────────────────────────────────────

# Module → color mapping
MODULE_COLOR = {
    "Authentication":    C_AUTH,
    "Authorization":     C_AUTHZ,
    "Navigation":        C_NAV,
    "UI Validation":     C_UI,
    "Forms":             C_FORM,
    "Input Validation":  C_FORM,
    "File Upload":       C_FILE,
    "History":           C_HIST,
    "Profile":           C_PROF,
    "Reset Password":    C_PROF,
    "Session":           C_SKIP,
    "Regression":        C_REG,
    "Performance":       C_PERF,
    "Accessibility":     C_ACC,
    "Responsive":        C_RESP,
}

PRIORITY_COLOR = {
    "Critical": "FFDC3545",
    "High":     "FFFD7E14",
    "Medium":   "FFFFC107",
    "Low":      "FF28A745",
}

STATUS_COLOR = {
    "Active":  "FF28A745",
    "Blocked": "FFDC3545",
    "Draft":   "FF6C757D",
}

def build_workbook(tests):
    wb = openpyxl.Workbook()

    # ── Sheet 1: All Test Cases ───────────────────────────────────────────────
    ws = wb.active
    ws.title = "All Test Cases"

    headers = ["TC ID","Module","Test Name","Objective","Precondition",
               "Test Steps","Expected Result","Priority","Status"]
    col_w   = [16,     18,      38,          45,          28,
               55,                35,              10,        10]

    # Header row
    for ci, (h, w) in enumerate(zip(headers, col_w), 1):
        c = ws.cell(1, ci, h)
        c.font      = hdr_font()
        c.fill      = fill(C_HEADER)
        c.alignment = cen()
        c.border    = bdr()
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[1].height = 22
    ws.freeze_panes = "A2"

    # Data rows
    for ri, row in enumerate(tests, 2):
        tc_id, module, name, obj, pre, steps, expected, priority, status = row
        mod_color  = MODULE_COLOR.get(module, C_HEADER)
        pri_color  = PRIORITY_COLOR.get(priority, "FFADB5BD")
        stat_color = STATUS_COLOR.get(status, "FF6C757D")
        bg = C_ROW_EVEN if ri % 2 == 0 else C_ROW_ODD

        for ci, val in enumerate(row, 1):
            cell = ws.cell(ri, ci, val)
            cell.font      = cell_font()
            cell.border    = bdr()
            cell.alignment = lft()
            cell.fill      = fill(bg)

        # Color TC ID column with module color
        ws.cell(ri, 1).fill = fill(mod_color)
        ws.cell(ri, 1).font = Font(name="Calibri", size=9, bold=True, color=C_WHITE)
        ws.cell(ri, 1).alignment = cen()

        # Color Priority column
        ws.cell(ri, 8).fill = fill(pri_color)
        ws.cell(ri, 8).font = Font(name="Calibri", size=9, bold=True, color=C_WHITE)
        ws.cell(ri, 8).alignment = cen()

        # Color Status column
        ws.cell(ri, 9).fill = fill(stat_color)
        ws.cell(ri, 9).font = Font(name="Calibri", size=9, bold=True, color=C_WHITE)
        ws.cell(ri, 9).alignment = cen()

        ws.row_dimensions[ri].height = 30

    # ── Sheet 2: Summary by Module ────────────────────────────────────────────
    ws2 = wb.create_sheet("Summary by Module")
    s2_headers = ["Module","Total","Critical","High","Medium","Low"]
    for ci, h in enumerate(s2_headers, 1):
        c = ws2.cell(1, ci, h)
        c.font = hdr_font(); c.fill = fill(C_HEADER)
        c.alignment = cen(); c.border = bdr()
    ws2.row_dimensions[1].height = 22

    from collections import defaultdict
    mod_stats = defaultdict(lambda: {"total":0,"Critical":0,"High":0,"Medium":0,"Low":0})
    for row in tests:
        m, priority = row[1], row[7]
        mod_stats[m]["total"] += 1
        mod_stats[m][priority] = mod_stats[m].get(priority,0) + 1

    for ri, (m, s) in enumerate(sorted(mod_stats.items()), 2):
        bg = C_ROW_EVEN if ri % 2 == 0 else C_ROW_ODD
        vals = [m, s["total"], s["Critical"], s["High"], s["Medium"], s["Low"]]
        for ci, v in enumerate(vals, 1):
            cell = ws2.cell(ri, ci, v)
            cell.font = cell_font(bold=(ci==1))
            cell.border = bdr(); cell.alignment = cen()
            cell.fill = fill(bg)
        ws2.cell(ri, 1).fill = fill(MODULE_COLOR.get(m, C_HEADER))
        ws2.cell(ri, 1).font = Font(name="Calibri", size=9, bold=True, color=C_WHITE)
        ws2.row_dimensions[ri].height = 18

    for ci, w in zip(range(1,7), [22,8,10,8,10,8]):
        ws2.column_dimensions[get_column_letter(ci)].width = w

    # ── Sheet 3: Critical Tests only ─────────────────────────────────────────
    ws3 = wb.create_sheet("Critical Tests")
    critical = [r for r in tests if r[7] == "Critical"]
    for ci, h in enumerate(headers, 1):
        c = ws3.cell(1, ci, h)
        c.font = hdr_font(); c.fill = fill("FFDC3545")
        c.alignment = cen(); c.border = bdr()
    ws3.freeze_panes = "A2"; ws3.row_dimensions[1].height = 22
    for ri, row in enumerate(critical, 2):
        for ci, val in enumerate(row, 1):
            cell = ws3.cell(ri, ci, val)
            cell.font = cell_font(); cell.border = bdr()
            cell.alignment = lft(); cell.fill = fill("FFFFF0F0")
        ws3.cell(ri, 1).fill = fill(MODULE_COLOR.get(row[1], C_HEADER))
        ws3.cell(ri, 1).font = Font(name="Calibri", size=9, bold=True, color=C_WHITE)
        ws3.cell(ri, 1).alignment = cen()
        ws3.row_dimensions[ri].height = 28
    for ci, w in zip(range(1,10), [16,18,38,45,28,55,35,10,10]):
        ws3.column_dimensions[get_column_letter(ci)].width = w

    # ── Sheet 4: Metrics ──────────────────────────────────────────────────────
    ws4 = wb.create_sheet("Metrics")
    total = len(tests)
    metrics = [
        ("Generated",       datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("Project",         "DentAI — Dental AI Platform"),
        ("Repository",      "https://github.com/kanishka1305/PDD"),
        ("Framework",       "Selenium + Python + pytest"),
        ("Total Tests",     total),
        ("Critical",        sum(1 for r in tests if r[7]=="Critical")),
        ("High",            sum(1 for r in tests if r[7]=="High")),
        ("Medium",          sum(1 for r in tests if r[7]=="Medium")),
        ("Low",             sum(1 for r in tests if r[7]=="Low")),
        ("Modules",         len(set(r[1] for r in tests))),
        ("Auth Tests",      sum(1 for r in tests if r[1]=="Authentication")),
        ("Security Tests",  sum(1 for r in tests if r[1]=="Authorization")),
        ("Regression Tests",sum(1 for r in tests if r[1]=="Regression")),
        ("Upload Tests",    sum(1 for r in tests if r[1]=="File Upload")),
        ("Profile Tests",   sum(1 for r in tests if r[1] in ("Profile","Reset Password"))),
        ("UI Tests",        sum(1 for r in tests if r[1]=="UI Validation")),
        ("Perf Tests",      sum(1 for r in tests if r[1]=="Performance")),
        ("Accessibility",   sum(1 for r in tests if r[1]=="Accessibility")),
        ("Responsive",      sum(1 for r in tests if r[1]=="Responsive")),
        ("Session Tests",   sum(1 for r in tests if r[1]=="Session")),
    ]
    for ci, h in enumerate(["Metric","Value"], 1):
        c = ws4.cell(1, ci, h)
        c.font = hdr_font(); c.fill = fill(C_HEADER)
        c.alignment = cen(); c.border = bdr()
    ws4.row_dimensions[1].height = 22
    for ri, (k, v) in enumerate(metrics, 2):
        bg = C_ROW_EVEN if ri % 2 == 0 else C_ROW_ODD
        ws4.cell(ri, 1, k).font = cell_font(bold=True)
        ws4.cell(ri, 2, v).font = cell_font()
        for ci in [1,2]:
            ws4.cell(ri, ci).border = bdr()
            ws4.cell(ri, ci).fill   = fill(bg)
            ws4.cell(ri, ci).alignment = lft()
        ws4.row_dimensions[ri].height = 18
    ws4.column_dimensions["A"].width = 26
    ws4.column_dimensions["B"].width = 45

    return wb


if __name__ == "__main__":
    out_path = "DentAI_All_Test_Cases.xlsx"
    wb = build_workbook(ALL_TESTS)
    wb.save(out_path)
    size = __import__("os").path.getsize(out_path)
    print(f"\n✓ Saved: {out_path}")
    print(f"  Total test cases : {len(ALL_TESTS)}")
    print(f"  File size        : {size:,} bytes ({size//1024} KB)")
    print(f"  Sheets           : All Test Cases | Summary by Module | Critical Tests | Metrics")
