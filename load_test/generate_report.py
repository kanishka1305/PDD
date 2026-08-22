"""
DentAI Load Test — Excel Report Generator
Reads Locust CSV output and produces a professional .xlsx report
"""
import csv, sys, os, datetime
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.series import DataPoint

# ── Colour palette ────────────────────────────────────────────────────────────
BLUE_DARK   = "1E3A5F"
BLUE_MED    = "2563EB"
BLUE_LIGHT  = "DBEAFE"
CYAN        = "0EA5E9"
GREEN       = "16A34A"
GREEN_LIGHT = "DCFCE7"
RED         = "DC2626"
RED_LIGHT   = "FEE2E2"
AMBER       = "D97706"
AMBER_LIGHT = "FEF3C7"
WHITE       = "FFFFFF"
GREY_LIGHT  = "F1F5F9"
GREY_MED    = "CBD5E1"
HEADER_FG   = "FFFFFF"

def side(style="thin", color="CBD5E1"):
    return Side(style=style, color=color)

def border(all_sides="thin"):
    s = side(all_sides)
    return Border(left=s, right=s, top=s, bottom=s)

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def hdr_font(size=10, bold=True, color=WHITE):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def cell_font(size=10, bold=False, color="1E293B"):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def set_col_width(ws, col, width):
    ws.column_dimensions[get_column_letter(col)].width = width

def read_stats_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def safe_float(val, default=0.0):
    try: return float(val)
    except: return default

def safe_int(val, default=0):
    try: return int(float(val))
    except: return default

def status_fill(avg_ms):
    if avg_ms == 0:   return fill(GREY_LIGHT)
    if avg_ms < 300:  return fill(GREEN_LIGHT)
    if avg_ms < 800:  return fill(AMBER_LIGHT)
    return fill(RED_LIGHT)

def status_label(avg_ms):
    if avg_ms == 0:   return "—"
    if avg_ms < 300:  return "✓ Excellent"
    if avg_ms < 800:  return "⚠ Acceptable"
    return "✗ Slow"

def status_label_rps(rps):
    if rps == 0:    return "—"
    if rps >= 50:   return "✓ Excellent"
    if rps >= 20:   return "⚠ Acceptable"
    return "✗ Low"

def write_cover(wb, meta):
    ws = wb.active
    ws.title = "Cover"
    ws.sheet_view.showGridLines = False

    # Header banner
    for r in range(1, 8):
        for c in range(1, 12):
            ws.cell(r, c).fill = fill(BLUE_DARK)

    ws.merge_cells("B2:K3")
    t = ws.cell(2, 2, "DentAI — Baseline Load Test Report")
    t.font      = Font("Calibri", size=22, bold=True, color=WHITE)
    t.alignment = Alignment(horizontal="left", vertical="center")

    ws.merge_cells("B4:K5")
    s = ws.cell(4, 2, "CBCT AI Segmentation Platform  ·  Performance Benchmark")
    s.font      = Font("Calibri", size=13, color=CYAN)
    s.alignment = Alignment(horizontal="left", vertical="center")

    ws.merge_cells("B6:K6")
    d = ws.cell(6, 2, "Generated: " + meta["generated"])
    d.font      = Font("Calibri", size=10, color=GREY_LIGHT)
    d.alignment = Alignment(horizontal="left", vertical="center")

    # Summary box
    summary = [
        ("Target URL",            meta["host"]),
        ("Virtual Users",         "100 concurrent users"),
        ("Test Duration",         "60 seconds"),
        ("Total Requests",        f"{meta['total_reqs']:,}"),
        ("Failed Requests",       f"{meta['total_fails']:,}"),
        ("Failure Rate",          f"{meta['fail_pct']:.1f}%"),
        ("Overall RPS",           f"{meta['overall_rps']:.1f} req/sec"),
        ("Avg Response Time",     f"{meta['avg_rt']:.0f} ms"),
        ("95th Percentile",       f"{meta['p95']:.0f} ms"),
    ]

    row = 9
    ws.merge_cells(f"B{row}:C{row}")
    h = ws.cell(row, 2, "TEST CONFIGURATION & SUMMARY")
    h.font = Font("Calibri", size=11, bold=True, color=BLUE_DARK)
    h.fill = fill(BLUE_LIGHT)
    h.alignment = Alignment(horizontal="left")
    ws.merge_cells(f"D{row}:K{row}")

    for i, (label, value) in enumerate(summary):
        r = row + 1 + i
        lc = ws.cell(r, 2, label)
        lc.font      = Font("Calibri", size=10, bold=True, color=BLUE_DARK)
        lc.fill      = fill(GREY_LIGHT)
        lc.alignment = Alignment(horizontal="left", indent=1)
        lc.border    = border()
        ws.merge_cells(f"C{r}:K{r}")
        vc = ws.cell(r, 3, value)
        vc.font      = Font("Calibri", size=10, color="1E293B")
        vc.alignment = Alignment(horizontal="left", indent=1)
        vc.border    = border()

    # Row heights
    for r in range(1, 8):  ws.row_dimensions[r].height = 18
    ws.row_dimensions[2].height = 36
    ws.row_dimensions[4].height = 24
    ws.row_dimensions[9].height = 20

    for c in range(1, 12): set_col_width(ws, c, 18)
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 26
    ws.row_dimensions[1].height = 6

def write_endpoint_table(wb, rows):
    ws = wb.create_sheet("Endpoint Results")
    ws.sheet_view.showGridLines = False

    # Title
    ws.merge_cells("A1:L1")
    t = ws.cell(1, 1, "DentAI — Endpoint Performance Results (100 Users · 60s)")
    t.font = Font("Calibri", size=14, bold=True, color=WHITE)
    t.fill = fill(BLUE_MED)
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    headers = [
        "Endpoint", "Method", "# Requests", "# Failures",
        "Fail %", "Avg (ms)", "Min (ms)", "Max (ms)",
        "Median (ms)", "90th % (ms)", "95th % (ms)", "Status"
    ]

    widths = [38, 8, 12, 12, 8, 11, 11, 11, 12, 14, 14, 14]

    for c, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(2, c, h)
        cell.font      = hdr_font(10)
        cell.fill      = fill(BLUE_DARK)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border    = border()
        set_col_width(ws, c, w)
    ws.row_dimensions[2].height = 32

    # Data rows (skip Aggregated row for main table)
    data_rows = [r for r in rows if r.get("Name","").strip() != "Aggregated"]
    # Put Aggregated at the end
    agg = [r for r in rows if r.get("Name","").strip() == "Aggregated"]
    data_rows = data_rows + agg

    for i, row in enumerate(data_rows):
        r = i + 3
        is_agg = row.get("Name","").strip() == "Aggregated"
        avg_ms = safe_float(row.get("Average Response Time", 0))

        values = [
            row.get("Name",""),
            row.get("Type","GET"),
            safe_int(row.get("Request Count", 0)),
            safe_int(row.get("Failure Count", 0)),
            f"{(safe_int(row.get('Failure Count',0)) / max(safe_int(row.get('Request Count',1)),1) * 100):.1f}%",
            f"{avg_ms:.0f}",
            f"{safe_float(row.get('Min Response Time',0)):.0f}",
            f"{safe_float(row.get('Max Response Time',0)):.0f}",
            f"{safe_float(row.get('Median Response Time',0)):.0f}",
            f"{safe_float(row.get('90%',0)):.0f}",
            f"{safe_float(row.get('95%',0)):.0f}",
            status_label(avg_ms),
        ]

        row_fill = fill(BLUE_LIGHT if is_agg else (GREY_LIGHT if i % 2 == 0 else WHITE))
        row_font = Font("Calibri", size=10, bold=is_agg, color="1E293B")

        for c, val in enumerate(values, 1):
            cell = ws.cell(r, c, val)
            cell.font      = row_font
            cell.border    = border()
            cell.alignment = Alignment(horizontal="center" if c > 1 else "left", indent=1 if c == 1 else 0)
            # Colour-code status and avg columns
            if c == 12:
                if "Excellent" in str(val): cell.fill = fill(GREEN_LIGHT); cell.font = Font("Calibri", size=10, bold=True, color=GREEN)
                elif "Acceptable" in str(val): cell.fill = fill(AMBER_LIGHT); cell.font = Font("Calibri", size=10, bold=True, color=AMBER)
                elif "Slow" in str(val): cell.fill = fill(RED_LIGHT); cell.font = Font("Calibri", size=10, bold=True, color=RED)
                else: cell.fill = fill(GREY_LIGHT)
            elif c == 6:   cell.fill = status_fill(avg_ms)
            else:          cell.fill = row_fill

        ws.row_dimensions[r].height = 18

    return ws

def write_charts(wb, rows):
    ws = wb.create_sheet("Charts")
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:P1")
    t = ws.cell(1, 1, "DentAI — Load Test Visual Analysis")
    t.font = Font("Calibri", size=14, bold=True, color=WHITE)
    t.fill = fill(BLUE_MED)
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    # Write hidden data table for charts
    data_rows = [r for r in rows if r.get("Name","").strip() not in ("", "Aggregated")]
    ws.cell(3, 1, "Endpoint").font    = hdr_font(9)
    ws.cell(3, 2, "Avg (ms)").font    = hdr_font(9)
    ws.cell(3, 3, "95th % (ms)").font = hdr_font(9)
    ws.cell(3, 4, "Requests").font    = hdr_font(9)
    for c in range(1,5):
        ws.cell(3, c).fill = fill(BLUE_DARK)
        ws.cell(3, c).alignment = Alignment(horizontal="center")

    for i, row in enumerate(data_rows, 4):
        name = row.get("Name","")[:30]
        ws.cell(i, 1, name)
        ws.cell(i, 2, safe_float(row.get("Average Response Time", 0)))
        ws.cell(i, 3, safe_float(row.get("95%", 0)))
        ws.cell(i, 4, safe_int(row.get("Request Count", 0)))

    n = len(data_rows)
    if n == 0: return

    # ── Bar chart: Response times ─────────────────────────────────────────────
    bar = BarChart()
    bar.type     = "col"
    bar.title    = "Average vs 95th Percentile Response Time (ms)"
    bar.y_axis.title = "Response Time (ms)"
    bar.x_axis.title = "Endpoint"
    bar.style    = 10
    bar.width    = 22; bar.height = 12

    avg_data  = Reference(ws, min_col=2, min_row=3, max_row=3+n)
    p95_data  = Reference(ws, min_col=3, min_row=3, max_row=3+n)
    cats      = Reference(ws, min_col=1, min_row=4, max_row=3+n)

    s1 = bar.__class__.__mro__[0]
    from openpyxl.chart import Series
    bar.add_data(avg_data, titles_from_data=True)
    bar.add_data(p95_data, titles_from_data=True)
    bar.set_categories(cats)
    bar.series[0].graphicalProperties.solidFill = "2563EB"
    bar.series[1].graphicalProperties.solidFill = "0EA5E9"
    ws.add_chart(bar, "A5")

    # ── Bar chart: Request count ──────────────────────────────────────────────
    bar2 = BarChart()
    bar2.type     = "col"
    bar2.title    = "Total Requests per Endpoint"
    bar2.y_axis.title = "Request Count"
    bar2.style    = 10
    bar2.width    = 22; bar2.height = 12

    req_data = Reference(ws, min_col=4, min_row=3, max_row=3+n)
    bar2.add_data(req_data, titles_from_data=True)
    bar2.set_categories(cats)
    bar2.series[0].graphicalProperties.solidFill = "16A34A"
    ws.add_chart(bar2, "L5")

def write_summary_kpi(wb, meta):
    ws = wb.create_sheet("KPI Summary")
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:J1")
    t = ws.cell(1, 1, "DentAI — Load Test KPI Dashboard")
    t.font = Font("Calibri", size=14, bold=True, color=WHITE)
    t.fill = fill(BLUE_DARK)
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    kpis = [
        ("Total Requests Sent",    f"{meta['total_reqs']:,}",        BLUE_LIGHT,  BLUE_MED),
        ("Failed Requests",        f"{meta['total_fails']:,}",        RED_LIGHT,   RED),
        ("Failure Rate",           f"{meta['fail_pct']:.1f}%",        AMBER_LIGHT, AMBER),
        ("Overall RPS",            f"{meta['overall_rps']:.1f} r/s",  GREEN_LIGHT, GREEN),
        ("Avg Response Time",      f"{meta['avg_rt']:.0f} ms",        BLUE_LIGHT,  BLUE_MED),
        ("Min Response Time",      f"{meta['min_rt']:.0f} ms",        GREEN_LIGHT, GREEN),
        ("Max Response Time",      f"{meta['max_rt']:.0f} ms",        RED_LIGHT,   RED),
        ("50th Percentile (P50)",  f"{meta['p50']:.0f} ms",           BLUE_LIGHT,  BLUE_MED),
        ("90th Percentile (P90)",  f"{meta['p90']:.0f} ms",           AMBER_LIGHT, AMBER),
        ("95th Percentile (P95)",  f"{meta['p95']:.0f} ms",           AMBER_LIGHT, AMBER),
    ]

    col = 1
    row_start = 3
    for i, (label, value, bg, accent) in enumerate(kpis):
        c = (i % 5) * 2 + 1
        r = row_start + (i // 5) * 5

        # Label cell
        lc = ws.cell(r, c, label)
        lc.font      = Font("Calibri", size=10, bold=True, color=accent)
        lc.fill      = fill(bg)
        lc.alignment = Alignment(horizontal="center", vertical="center")
        lc.border    = border()
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+1)
        ws.row_dimensions[r].height = 18

        # Value cell
        vc = ws.cell(r+1, c, value)
        vc.font      = Font("Calibri", size=20, bold=True, color=accent)
        vc.fill      = fill(bg)
        vc.alignment = Alignment(horizontal="center", vertical="center")
        vc.border    = border()
        ws.merge_cells(start_row=r+1, start_column=c, end_row=r+3, end_column=c+1)
        ws.row_dimensions[r+1].height = 36
        ws.row_dimensions[r+2].height = 36
        ws.row_dimensions[r+3].height = 36

    for c in range(1, 12): set_col_width(ws, c, 16)

    # SLA verdict
    row_v = row_start + 12
    ws.merge_cells(f"A{row_v}:J{row_v}")
    avg = meta['avg_rt']
    fail = meta['fail_pct']
    if avg < 300 and fail < 1:
        verdict = "✓  PASS — Response times excellent and failure rate below threshold"
        vfill, vcolor = GREEN_LIGHT, GREEN
    elif avg < 800 and fail < 5:
        verdict = "⚠  MARGINAL — Acceptable performance but room for optimization"
        vfill, vcolor = AMBER_LIGHT, AMBER
    else:
        verdict = "✗  FAIL — Response times or failure rate exceed SLA thresholds"
        vfill, vcolor = RED_LIGHT, RED

    vc = ws.cell(row_v, 1, verdict)
    vc.font      = Font("Calibri", size=13, bold=True, color=vcolor)
    vc.fill      = fill(vfill)
    vc.alignment = Alignment(horizontal="center", vertical="center")
    vc.border    = border("medium")
    ws.row_dimensions[row_v].height = 28

def write_raw_data(wb, rows):
    ws = wb.create_sheet("Raw Data")
    if not rows: return
    headers = list(rows[0].keys())
    for c, h in enumerate(headers, 1):
        cell = ws.cell(1, c, h)
        cell.font = hdr_font(9)
        cell.fill = fill(BLUE_DARK)
        cell.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(c)].width = max(len(h)+2, 14)
    for r, row in enumerate(rows, 2):
        for c, key in enumerate(headers, 1):
            ws.cell(r, c, row.get(key, ""))
            ws.cell(r, c).font = Font("Calibri", size=9)
            ws.cell(r, c).fill = fill(GREY_LIGHT if r % 2 == 0 else WHITE)
            ws.cell(r, c).alignment = Alignment(horizontal="center")


def generate_excel(stats_csv_path: str, history_csv_path: str, output_path: str):
    rows = read_stats_csv(stats_csv_path)
    if not rows:
        print("ERROR: Stats CSV is empty or not found.")
        return

    agg   = next((r for r in rows if r.get("Name","").strip() == "Aggregated"), {})
    total_reqs  = safe_int(agg.get("Request Count", 0))
    total_fails = safe_int(agg.get("Failure Count", 0))
    fail_pct    = (total_fails / max(total_reqs, 1)) * 100
    avg_rt      = safe_float(agg.get("Average Response Time", 0))
    min_rt      = safe_float(agg.get("Min Response Time", 0))
    max_rt      = safe_float(agg.get("Max Response Time", 0))
    p50         = safe_float(agg.get("50%", 0))
    p90         = safe_float(agg.get("90%", 0))
    p95         = safe_float(agg.get("95%", 0))
    rps         = safe_float(agg.get("Requests/s", 0))

    meta = dict(
        host="http://localhost:8000",
        generated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_reqs=total_reqs, total_fails=total_fails,
        fail_pct=fail_pct, overall_rps=rps,
        avg_rt=avg_rt, min_rt=min_rt, max_rt=max_rt,
        p50=p50, p90=p90, p95=p95,
    )

    wb = Workbook()
    write_cover(wb, meta)
    write_endpoint_table(wb, rows)
    write_charts(wb, rows)
    write_summary_kpi(wb, meta)
    write_raw_data(wb, rows)

    wb.save(output_path)
    print(f"Excel report saved: {output_path}")


if __name__ == "__main__":
    base = Path(__file__).parent
    generate_excel(
        str(base / "results" / "stats_stats.csv"),
        str(base / "results" / "stats_stats_history.csv"),
        str(base / "results" / "DentAI_LoadTest_Report.xlsx"),
    )
