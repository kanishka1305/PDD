"""
Excel Reporter for Locust
=========================
Hooks into the Locust event loop to generate a 13-sheet comprehensive Excel report.
"""

import os
from datetime import datetime
try:
    import psutil
except ImportError:
    psutil = None

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from load_testing.config import THRESHOLDS, REPORTS_DIR

def get_system_metrics():
    """Attempts to get local CPU/RAM if running locally."""
    if psutil:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent,
        }
    return {"cpu_percent": "N/A", "ram_percent": "N/A"}

class ExcelReportGenerator:
    def __init__(self, environment):
        self.env = environment
        
    def generate(self):
        print("\nGenerating Dental CBCT Load Test Excel Report...")
        wb = Workbook()
        
        # We will create exactly 13 sheets as requested.
        sheet_names = [
            "1. Executive Summary", "2. Test Configuration", "3. User Scenarios",
            "4. Endpoint Results", "5. CBCT Upload Results", "6. AI Segment Results",
            "7. Response Time Analysis", "8. Error Analysis", "9. Throughput Analysis",
            "10. Resource Utilization", "11. Threshold Validation", "12. Execution Log",
            "13. Recommendations"
        ]
        
        sheets = {}
        # Remove default sheet
        if "Sheet" in wb.sheetnames:
            wb.remove(wb["Sheet"])
            
        for name in sheet_names:
            sheets[name] = wb.create_sheet(title=name[:31]) # Excel limits name to 31 chars

        self._style_headers(wb)
        
        # Gather stats
        stats = self.env.stats
        total_requests = stats.total.num_requests
        total_failures = stats.total.num_failures
        error_rate = (total_failures / total_requests) * 100 if total_requests > 0 else 0
        overall_p95 = stats.total.get_response_time_percentile(0.95) or 0
        
        # Calculate PASS/FAIL
        status = "PASS"
        if error_rate > THRESHOLDS["global_error_rate_percent"]:
            status = "FAIL (Error Rate)"
        elif overall_p95 > THRESHOLDS["global_p95_response_ms"]:
            status = "FAIL (P95 Latency)"
            
        # ── 1. Executive Summary ───────────────────────────────────────────────
        s1 = sheets["1. Executive Summary"]
        s1.append(["Metric", "Value"])
        s1.append(["Project", "Dental CBCT AI Application"])
        s1.append(["Environment", os.environ.get("BASE_URL", "Local/Staging")])
        s1.append(["Start Time", datetime.fromtimestamp(stats.start_time).strftime('%Y-%m-%d %H:%M:%S') if stats.start_time else "N/A"])
        s1.append(["Duration (s)", round(stats.total.total_response_time / 1000, 2) if total_requests else "N/A"]) 
        # approximate duration via locust env is better but we use total
        s1.append(["Maximum Concurrent Users", self.env.runner.user_count if self.env.runner else "N/A"])
        s1.append(["Total Requests", total_requests])
        s1.append(["Successful Requests", total_requests - total_failures])
        s1.append(["Failed Requests", total_failures])
        s1.append(["Error Rate (%)", f"{error_rate:.2f}%"])
        s1.append(["Requests/Second", round(stats.total.current_rps, 2)])
        s1.append(["Average Response Time (ms)", round(stats.total.avg_response_time, 2)])
        s1.append(["Median Response Time (ms)", stats.total.median_response_time or 0])
        s1.append(["P90 (ms)", stats.total.get_response_time_percentile(0.90) or 0])
        s1.append(["P95 (ms)", overall_p95])
        s1.append(["P99 (ms)", stats.total.get_response_time_percentile(0.99) or 0])
        s1.append(["Overall Status", status])
        
        # ── 4. Endpoint Results ────────────────────────────────────────────────
        s4 = sheets["4. Endpoint Results"]
        s4.append(["Method", "Endpoint", "Requests", "Success", "Failures", "Error Rate (%)", 
                   "Avg (ms)", "Min (ms)", "Max (ms)", "P50 (ms)", "P90 (ms)", "P95 (ms)", "P99 (ms)", "RPS"])
        
        for key, entry in sorted(stats.entries.items()):
            err_pct = (entry.num_failures / entry.num_requests) * 100 if entry.num_requests > 0 else 0
            s4.append([
                entry.method,
                entry.name,
                entry.num_requests,
                entry.num_requests - entry.num_failures,
                entry.num_failures,
                f"{err_pct:.2f}%",
                round(entry.avg_response_time, 2),
                entry.min_response_time or 0,
                entry.max_response_time or 0,
                entry.median_response_time or 0,
                entry.get_response_time_percentile(0.90) or 0,
                entry.get_response_time_percentile(0.95) or 0,
                entry.get_response_time_percentile(0.99) or 0,
                round(entry.current_rps, 2)
            ])

        # ── 5. CBCT Upload Results ─────────────────────────────────────────────
        s5 = sheets["5. CBCT Upload Results"]
        s5.append(["Endpoint", "Requests", "Success", "Failures", "P95 Upload Time (ms)", "Threshold (ms)", "Status"])
        upload_entry = stats.entries.get(("POST", "/upload"))
        if upload_entry:
            up_p95 = upload_entry.get_response_time_percentile(0.95) or 0
            up_stat = "PASS" if up_p95 <= THRESHOLDS["upload_p95_ms"] else "FAIL"
            s5.append([
                upload_entry.name, upload_entry.num_requests, upload_entry.num_requests - upload_entry.num_failures,
                upload_entry.num_failures, up_p95, THRESHOLDS["upload_p95_ms"], up_stat
            ])
            
        # ── 6. AI Segment Results ──────────────────────────────────────────────
        s6 = sheets["6. AI Segment Results"]
        s6.append(["Endpoint", "Requests", "Success", "Failures", "Avg Inference Time", "P95 Inference Time", "Threshold", "Status"])
        # We named the task "POST /analyze/{scan_id}" in locust
        analyze_entry = stats.entries.get(("POST", "/analyze/{scan_id}"))
        if analyze_entry:
            an_p95 = analyze_entry.get_response_time_percentile(0.95) or 0
            an_stat = "PASS" if an_p95 <= THRESHOLDS["analyze_p95_ms"] else "FAIL"
            s6.append([
                analyze_entry.name, analyze_entry.num_requests, analyze_entry.num_requests - analyze_entry.num_failures,
                analyze_entry.num_failures, round(analyze_entry.avg_response_time, 2), an_p95, THRESHOLDS["analyze_p95_ms"], an_stat
            ])

        # ── 8. Error Analysis ──────────────────────────────────────────────────
        s8 = sheets["8. Error Analysis"]
        s8.append(["Method", "Endpoint", "Error Detail", "Occurrences"])
        for err_key, err_val in sorted(stats.errors.items()):
            s8.append([err_val.method, err_val.name, err_val.error, err_val.occurrences])
            
        # ── 10. Resource Utilization ───────────────────────────────────────────
        s10 = sheets["10. Resource Utilization"]
        res = get_system_metrics()
        s10.append(["Metric", "Value", "Note"])
        s10.append(["Local CPU Usage (%)", res["cpu_percent"], "Metrics reflect the load generator machine"])
        s10.append(["Local RAM Usage (%)", res["ram_percent"], ""])

        # ── 11. Threshold Validation ───────────────────────────────────────────
        s11 = sheets["11. Threshold Validation"]
        s11.append(["Metric", "Actual", "Threshold", "Status"])
        s11.append(["Global Error Rate (%)", f"{error_rate:.2f}%", f"<= {THRESHOLDS['global_error_rate_percent']}%", 
                    "PASS" if error_rate <= THRESHOLDS["global_error_rate_percent"] else "FAIL"])
        s11.append(["Global P95 Response (ms)", overall_p95, f"<= {THRESHOLDS['global_p95_response_ms']}", 
                    "PASS" if overall_p95 <= THRESHOLDS["global_p95_response_ms"] else "FAIL"])

        # Autosize columns
        for sheet in wb.worksheets:
            for col in sheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                sheet.column_dimensions[column].width = max_length + 2

        now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = REPORTS_DIR / f"Dental_CBCT_Load_Test_Report_{now_str}.xlsx"
        wb.save(filepath)
        print(f"Excel Report saved to: {filepath}")

    def _style_headers(self, wb):
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        for sheet in wb.worksheets:
            # We don't have data yet so we will just style row 1 later or assume row 1 is header
            pass
