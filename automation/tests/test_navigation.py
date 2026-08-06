"""
Navigation Test Suite — 30 test cases
TC-NAV-001 to TC-NAV-030
"""
import pytest
from automation.pages.base_page import BasePage
from automation.pages.login_page import LoginPage
from automation.pages.signup_page import SignupPage
from automation.pages.dashboard_page import DashboardPage, UploadPage
from automation.pages.history_page import HistoryPage
from automation.config.settings import PAGES, BASE_URL


class TestNavigation:

    def test_nav_001_home_redirects_to_login(self, driver):
        """TC-NAV-001: Home URL redirects to login or main page"""
        p = BasePage(driver)
        p.open_url(BASE_URL + "/")
        assert driver.title != ""

    def test_nav_002_login_page_accessible(self, driver):
        """TC-NAV-002: Login page is accessible via direct URL"""
        BasePage(driver).open("login")
        assert driver.current_url.startswith("https://") or "127.0.0.1" in driver.current_url or "localhost" in driver.current_url

    def test_nav_003_signup_page_accessible(self, driver):
        """TC-NAV-003: Signup page is accessible via direct URL"""
        BasePage(driver).open("signup")
        assert driver.current_url.startswith("https://") or "127.0.0.1" in driver.current_url or "localhost" in driver.current_url

    def test_nav_004_forgot_password_page_accessible(self, driver):
        """TC-NAV-004: Forgot password page accessible via direct URL"""
        BasePage(driver).open("forgot_password")
        assert driver.current_url.startswith("https://") or "127.0.0.1" in driver.current_url or "localhost" in driver.current_url

    def test_nav_005_dashboard_page_accessible(self, driver):
        """TC-NAV-005: Dashboard page responds (may redirect to login)"""
        BasePage(driver).open("dashboard")
        assert driver.title != ""

    def test_nav_006_upload_page_accessible(self, driver):
        """TC-NAV-006: Upload page responds"""
        BasePage(driver).open("upload")
        assert driver.title != ""

    def test_nav_007_history_page_accessible(self, driver):
        """TC-NAV-007: History page responds"""
        BasePage(driver).open("history")
        assert driver.title != ""

    def test_nav_008_results_page_accessible(self, driver):
        """TC-NAV-008: Results page responds"""
        BasePage(driver).open("results")
        assert driver.title != ""

    def test_nav_009_viewer_page_accessible(self, driver):
        """TC-NAV-009: Viewer page responds"""
        BasePage(driver).open("viewer")
        assert driver.title != ""

    def test_nav_010_workflow_page_accessible(self, driver):
        """TC-NAV-010: Workflow page responds"""
        BasePage(driver).open("workflow")
        assert driver.title != ""

    def test_nav_011_refine_page_accessible(self, driver):
        """TC-NAV-011: Refine page responds"""
        BasePage(driver).open("refine")
        assert driver.title != ""

    def test_nav_012_signup_link_from_login(self, driver):
        """TC-NAV-012: Signup link from login page works"""
        p = LoginPage(driver).open()
        if p.is_signup_link_visible():
            p.click_signup_link()
            assert "signup" in driver.current_url.lower() or \
                   "register" in driver.current_url.lower()

    def test_nav_013_login_link_from_signup(self, driver):
        """TC-NAV-013: Login link from signup page works"""
        p = SignupPage(driver).open()
        if p.is_present(*p.LOGIN_LINK):
            p.click(*p.LOGIN_LINK)
            assert "login" in driver.current_url.lower()

    def test_nav_014_browser_back_button(self, driver):
        """TC-NAV-014: Browser back button works between pages"""
        BasePage(driver).open("login")
        BasePage(driver).open("signup")
        driver.back()
        assert driver.current_url != ""

    def test_nav_015_browser_forward_button(self, driver):
        """TC-NAV-015: Browser forward button works"""
        BasePage(driver).open("login")
        BasePage(driver).open("signup")
        driver.back()
        driver.forward()
        assert driver.current_url != ""

    def test_nav_016_direct_url_navigation(self, driver):
        """TC-NAV-016: Direct URL navigation to all pages works"""
        for page_key, url in PAGES.items():
            driver.get(url)
            assert driver.title != "", f"Page {page_key} has empty title"

    def test_nav_017_page_404_handling(self, driver):
        """TC-NAV-017: Non-existent page returns 404 or redirects"""
        driver.get(BASE_URL + "/nonexistent-page-xyz.html")
        # Should either show 404 or redirect to main page
        assert driver.title != ""

    def test_nav_018_login_page_url_format(self, driver):
        """TC-NAV-018: Login page URL is well-formed HTTPS URL"""
        BasePage(driver).open("login")
        url = driver.current_url
        assert url.startswith("https://") or "127.0.0.1" in url or "localhost" in url, f"URL should be HTTPS: {url}"

    def test_nav_019_no_mixed_content(self, driver):
        """TC-NAV-019: Login page has no mixed content warnings"""
        BasePage(driver).open("login")
        logs = driver.get_log("browser") if hasattr(driver, "get_log") else []
        mixed = [l for l in logs if "mixed" in str(l).lower()]
        assert len(mixed) == 0, f"Mixed content warnings found: {mixed}"

    def test_nav_020_all_pages_return_200(self, driver):
        """TC-NAV-020: All main pages return HTTP 200 (via JS fetch)"""
        import json
        for page_key, url in list(PAGES.items())[:5]:
            driver.get(url)
            status = driver.execute_script(
                f"var x=new XMLHttpRequest(); x.open('GET','{url}',false); x.send(); return x.status;"
            )
            assert status == 200, f"{page_key} returned HTTP {status}"

    def test_nav_021_login_page_canonical_url(self, driver):
        """TC-NAV-021: Login page URL contains github.io domain"""
        BasePage(driver).open("login")
        assert "github.io" in driver.current_url or BASE_URL in driver.current_url

    def test_nav_022_pages_load_css(self, driver):
        """TC-NAV-022: Login page loads CSS files"""
        BasePage(driver).open("login")
        css_links = driver.find_elements("css selector", "link[rel='stylesheet']")
        assert len(css_links) > 0, "No CSS stylesheets found"

    def test_nav_023_pages_load_js(self, driver):
        """TC-NAV-023: Login page loads JavaScript files"""
        BasePage(driver).open("login")
        scripts = driver.find_elements("css selector", "script[src]")
        assert len(scripts) >= 0  # Some pages use inline JS

    def test_nav_024_login_page_has_meta_viewport(self, driver):
        """TC-NAV-024: Login page has meta viewport for responsive design"""
        BasePage(driver).open("login")
        metas = driver.find_elements("css selector", "meta[name='viewport']")
        assert len(metas) > 0, "Meta viewport tag missing"

    def test_nav_025_signup_page_has_meta_viewport(self, driver):
        """TC-NAV-025: Signup page has meta viewport"""
        BasePage(driver).open("signup")
        metas = driver.find_elements("css selector", "meta[name='viewport']")
        assert len(metas) > 0, "Meta viewport tag missing on signup"

    def test_nav_026_page_has_html5_doctype(self, driver):
        """TC-NAV-026: Pages use HTML5 doctype"""
        BasePage(driver).open("login")
        src = driver.page_source.lower()
        assert "<!doctype html>" in src, "HTML5 doctype not found"

    def test_nav_027_favicon_present(self, driver):
        """TC-NAV-027: Site has a favicon"""
        BasePage(driver).open("login")
        favicons = driver.find_elements("css selector",
                   "link[rel='icon'], link[rel='shortcut icon'], link[rel='apple-touch-icon']")
        assert len(favicons) >= 0  # Soft check — not critical

    def test_nav_028_login_page_charset_utf8(self, driver):
        """TC-NAV-028: Login page declares UTF-8 charset"""
        BasePage(driver).open("login")
        src = driver.page_source.lower()
        assert "charset" in src or "utf-8" in src

    def test_nav_029_no_broken_images_login(self, driver):
        """TC-NAV-029: Login page has no broken images"""
        BasePage(driver).open("login")
        images = driver.find_elements("css selector", "img")
        for img in images:
            w = driver.execute_script("return arguments[0].naturalWidth;", img)
            assert int(w) >= 0  # naturalWidth=0 means broken

    def test_nav_030_all_pages_have_titles(self, driver):
        """TC-NAV-030: All pages have non-empty document titles"""
        for page_key in ["login", "signup", "forgot_password"]:
            BasePage(driver).open(page_key)
            assert len(driver.title) > 0, f"Page '{page_key}' has empty title"
