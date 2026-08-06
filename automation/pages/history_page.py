"""
History, Results, Viewer Page Objects
"""
from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage


class HistoryPage(BasePage):
    SCAN_ROWS       = (By.CSS_SELECTOR, "tbody tr, .scan-row, .history-item, .list-item")
    SEARCH_INPUT    = (By.CSS_SELECTOR, "input[type='search'], .search-input, #search")
    FILTER_BTN      = (By.CSS_SELECTOR, ".filter-btn, .filter, select[name*='filter']")
    SORT_BTNS       = (By.CSS_SELECTOR, "th[data-sort], .sortable, .sort-btn")
    PATIENT_NAMES   = (By.CSS_SELECTOR, ".patient-name, td:first-child, [class*='patient']")
    DATE_CELLS      = (By.CSS_SELECTOR, ".date, td[class*='date'], [class*='created']")
    ACTION_BTNS     = (By.CSS_SELECTOR, ".action-btn, .view-btn, .analyze-btn, td a, td button")
    PAGINATION      = (By.CSS_SELECTOR, ".pagination, .pager, [class*='pagination']")
    EMPTY_STATE     = (By.CSS_SELECTOR, ".empty, .no-data, .empty-state, [class*='empty']")
    TABLE           = (By.CSS_SELECTOR, "table, .data-table, .scan-table")

    def open(self):
        return super().open("history")

    def is_on_history_page(self) -> bool:
        return "history" in self.get_current_url().lower()

    def get_scan_count(self) -> int:
        return self.element_count(*self.SCAN_ROWS)

    def is_table_visible(self) -> bool:
        return self.is_visible(*self.TABLE)

    def has_search(self) -> bool:
        return self.is_present(*self.SEARCH_INPUT)

    def has_pagination(self) -> bool:
        return self.is_present(*self.PAGINATION)


class ResultsPage(BasePage):
    STL_VIEWER      = (By.CSS_SELECTOR, ".stl-viewer, canvas, #viewer, [class*='viewer']")
    DOWNLOAD_BTN    = (By.CSS_SELECTOR, ".download-btn, a[download], button[class*='download']")
    METRICS         = (By.CSS_SELECTOR, ".metrics, .measurements, .results-data, [class*='metric']")
    REGION_TABS     = (By.CSS_SELECTOR, ".region-tab, .tab-btn, [role='tab']")
    BACK_BTN        = (By.CSS_SELECTOR, ".back-btn, a[href*='history'], button[class*='back']")
    EXPORT_BTN      = (By.CSS_SELECTOR, ".export-btn, button[class*='export'], a[class*='export']")
    PATIENT_INFO    = (By.CSS_SELECTOR, ".patient-info, .patient-details, [class*='patient']")
    REPORT_BTN      = (By.CSS_SELECTOR, ".report-btn, button[class*='report'], a[class*='report']")

    def open(self):
        return super().open("results")

    def is_on_results_page(self) -> bool:
        return "results" in self.get_current_url().lower()

    def has_viewer(self) -> bool:
        return self.is_present(*self.STL_VIEWER)

    def has_download_btn(self) -> bool:
        return self.is_present(*self.DOWNLOAD_BTN)

    def get_metrics_count(self) -> int:
        return self.element_count(*self.METRICS)


class ViewerPage(BasePage):
    CANVAS          = (By.CSS_SELECTOR, "canvas, #threejs-canvas, .three-canvas")
    CONTROLS        = (By.CSS_SELECTOR, ".viewer-controls, .controls, [class*='control']")
    REGION_SELECTOR = (By.CSS_SELECTOR, ".region-select, select, [class*='region']")
    ZOOM_IN         = (By.CSS_SELECTOR, ".zoom-in, button[class*='zoom-in'], #zoom-in")
    ZOOM_OUT        = (By.CSS_SELECTOR, ".zoom-out, button[class*='zoom-out'], #zoom-out")
    RESET_VIEW      = (By.CSS_SELECTOR, ".reset-view, button[class*='reset'], #reset")
    LOADING_SPINNER = (By.CSS_SELECTOR, ".loading, .spinner, [class*='loading']")
    FULLSCREEN_BTN  = (By.CSS_SELECTOR, ".fullscreen, button[class*='fullscreen']")

    def open(self):
        return super().open("viewer")

    def is_on_viewer_page(self) -> bool:
        return "viewer" in self.get_current_url().lower()

    def has_canvas(self) -> bool:
        return self.is_present(*self.CANVAS)

    def has_controls(self) -> bool:
        return self.is_present(*self.CONTROLS)
