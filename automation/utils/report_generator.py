"""
HTML + Excel Report Generator for Automation Results
"""
import json, os, sys
from datetime import datetime
from pathlib import Path
from automation.config.settings import (
    HTML_DIR, EXCEL_DIR, SUMMARY_DIR, JSON_DIR, BASE_URL
)


def generate_html_report(results: list, summary: dict, output_path: Path = None):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total    = summary.get("total", 0)
    passed   = summary.get("passed", 0)
    failed   = summary.get("failed", 0)
    skipped  = summary.get("skipped", 0)
    rate     = f"{passed/total*100:.1f}%" if total else "0%"
    duration = sum(r.get("duration", 0) for r in results)

    # Category breakdown
    cats = {}
    for r in results:
        m = r.get("module", "unknown")
        cats.setdefault(m, {"pass": 0, "fail": 0})
        if r.get("status") == "PASS":
            cats[m]["pass"] += 1
        else:
            cats[m]["fail"] += 1

    rows = ""
    for r in results:
        s = r.get("status", "UNKNOWN")
        bg = "#d4edda" if s == "PASS" else "#f8d7da" if s == "FAIL" else "#fff3cd"
        badge = f'<span style="background:{"#28a745" if s=="PASS" else "#dc3545" if s=="FAIL" else "#ffc107"};color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">{s}</span>'
        ss = ""
        if r.get("screenshot"):
            ss = f'<a href="{r["screenshot"]}" target="_blank">📷</a>'
        rows += f"""
        <tr style="background:{bg}">
          <td style="padding:6px;border:1px solid #dee2e6;font-size:12px">{r.get("test_id","")}</td>
          <td style="padding:6px;border:1px solid #dee2e6;font-size:12px">{r.get("module","")}</td>
          <td style="padding:6px;border:1px solid #dee2e6;font-size:12px">{r.get("name","")}</td>
          <td style="padding:6px;border:1px solid #dee2e6;text-align:center">{badge}</td>
          <td style="padding:6px;border:1px solid #dee2e6;text-align:right;font-size:12px">{r.get("duration",0):.2f}s</td>
          <td style="padding:6px;border:1px solid #dee2e6;font-size:11px;max-width:300px;overflow:hidden">{r.get("failure_reason","")[:200]}</td>
          <td style="padding:6px;border:1px solid #dee2e6;text-align:center">{ss}</td>
        </tr>"""

    cat_rows = ""
    for m, d in sorted(cats.items()):
        t = d["pass"] + d["fail"]
        p = f"{d['pass']/t*100:.0f}%" if t else "0%"
        bg = "#d4edda" if d["fail"] == 0 else "#f8d7da" if d["pass"] == 0 else "#fff3cd"
        cat_rows += f'<tr style="background:{bg}"><td style="padding:6px;border:1px solid #dee2e6">{m}</td><td style="text-align:center;padding:6px;border:1px solid #dee2e6">{t}</td><td style="text-align:center;padding:6px;border:1px solid #dee2e6;color:#28a745"><b>{d["pass"]}</b></td><td style="text-align:center;padding:6px;border:1px solid #dee2e6;color:#dc3545"><b>{d["fail"]}</b></td><td style="text-align:center;padding:6px;border:1px solid #dee2e6"><b>{p}</b></td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DentAI E2E Execution Report</title>
<style>
  body{{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f4f6f9;color:#333}}
  .header{{background:linear-gradient(135deg,#1a252f,#2c3e50);color:#fff;padding:30px 40px}}
  .header h1{{margin:0;font-size:28px}} .header p{{margin:5px 0;opacity:.8;font-size:14px}}
  .container{{max-width:1400px;margin:20px auto;padding:0 20px}}
  .cards{{display:grid;grid-template-columns:repeat(5,1fr);gap:15px;margin:20px 0}}
  .card{{background:#fff;border-radius:8px;padding:20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
  .card .num{{font-size:36px;font-weight:700;margin:8px 0}}
  .card .lbl{{font-size:13px;color:#666;text-transform:uppercase}}
  .section{{background:#fff;border-radius:8px;padding:20px;margin:20px 0;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
  h2{{color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:8px}}
  table{{width:100%;border-collapse:collapse}}
  th{{background:#2c3e50;color:#fff;padding:10px;text-align:left;font-size:13px}}
</style></head><body>
<div class="header">
  <h1>🦷 DentAI — E2E Automation Report</h1>
  <p>Deployment URL: <a href="{BASE_URL}" style="color:#3498db">{BASE_URL}</a></p>
  <p>Generated: {ts} | Framework: Selenium + Python + pytest</p>
</div>
<div class="container">
  <div class="cards">
    <div class="card"><div class="num" style="color:#2c3e50">{total}</div><div class="lbl">Total</div></div>
    <div class="card"><div class="num" style="color:#28a745">{passed}</div><div class="lbl">Passed</div></div>
    <div class="card"><div class="num" style="color:#dc3545">{failed}</div><div class="lbl">Failed</div></div>
    <div class="card"><div class="num" style="color:#ffc107">{skipped}</div><div class="lbl">Skipped</div></div>
    <div class="card"><div class="num" style="color:{"#28a745" if failed==0 else "#dc3545"}">{rate}</div><div class="lbl">Pass Rate</div></div>
  </div>
  <div class="section">
    <h2>📊 Results by Module</h2>
    <table><thead><tr><th>Module</th><th style="text-align:center">Total</th><th style="text-align:center">Pass</th><th style="text-align:center">Fail</th><th style="text-align:center">Rate</th></tr></thead>
    <tbody>{cat_rows}</tbody></table>
  </div>
  <div class="section">
    <h2>📋 All Test Results ({total} tests | Duration: {duration:.1f}s)</h2>
    <table><thead><tr><th>Test ID</th><th>Module</th><th>Test Name</th><th>Status</th><th>Duration</th><th>Failure Reason</th><th>SS</th></tr></thead>
    <tbody>{rows}</tbody></table>
  </div>
</div></body></html>"""

    if output_path is None:
        output_path = HTML_DIR / "execution-report.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def generate_excel_report(results: list, summary: dict):
    import openpyxl
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

    wb = openpyxl.Workbook()
    # ⚠️ openpyxl requires 8-character ARGB format: AARRGGBB (alpha + RGB)
    # Leading "FF" = fully opaque
    DK="FF1A252F"; GR="FFECF0F1"; WH="FFFFFFFF"
    PAS="FF28A745"; FAI="FFDC3545"; SKP="FFFFC107"

    def fill(c): return PatternFill("solid", fgColor=c)
    def hf(sz=11,bold=True,color=WH): return Font(name="Calibri",sz=sz,bold=bold,color=color)
    def cf(sz=10,bold=False,color=DK): return Font(name="Calibri",sz=sz,bold=bold,color=color)
    def cen(): return Alignment(horizontal="center",vertical="center",wrap_text=True)
    def lft(): return Alignment(horizontal="left",vertical="center",wrap_text=True)
    def bdr():
        # Border color also needs 8-char ARGB
        s=Side(style="thin",color="FFCCCCCC")
        return Border(left=s,right=s,top=s,bottom=s)

    def set_header(ws, headers, row=1, bg=DK):
        for i,h in enumerate(headers,1):
            c=ws.cell(row,i,h); c.font=hf(); c.fill=fill(bg)
            c.alignment=cen(); c.border=bdr()
        ws.row_dimensions[row].height=20

    def col_widths(ws, widths):
        from openpyxl.utils import get_column_letter
        for i,w in enumerate(widths,1):
            ws.column_dimensions[get_column_letter(i)].width=w

    # ── Sheet 1: All Tests ────────────────────────────────────────────────────
    ws1 = wb.active; ws1.title = "All Test Cases"
    headers = ["Test ID","Module","Test Name","Status","Duration(s)","Failure Reason","Screenshot","Timestamp"]
    set_header(ws1, headers, 1)
    for idx,r in enumerate(results,2):
        s=r.get("status","UNKNOWN")
        bg=PAS if s=="PASS" else FAI if s=="FAIL" else SKP
        vals=[r.get("test_id",""),r.get("module",""),r.get("name",""),s,
              r.get("duration",0),r.get("failure_reason","")[:200],
              r.get("screenshot",""),r.get("timestamp","")]
        for c,v in enumerate(vals,1):
            cell=ws1.cell(idx,c,v); cell.font=cf(); cell.border=bdr()
            cell.alignment=lft()
        sc=ws1.cell(idx,4); sc.fill=fill(bg)
        sc.font=Font(name="Calibri",sz=10,bold=True,color=WH); sc.alignment=cen()
        ws1.row_dimensions[idx].height=18
    col_widths(ws1,[30,22,50,10,12,50,40,22])
    ws1.freeze_panes="A2"

    # ── Sheet 2: Passed ───────────────────────────────────────────────────────
    ws2 = wb.create_sheet("Passed Tests")
    set_header(ws2, ["Test ID","Module","Test Name","Duration(s)","Timestamp"], bg=PAS)
    passed = [r for r in results if r.get("status")=="PASS"]
    for idx,r in enumerate(passed,2):
        vals=[r.get("test_id",""),r.get("module",""),r.get("name",""),r.get("duration",0),r.get("timestamp","")]
        for c,v in enumerate(vals,1):
            cell=ws2.cell(idx,c,v); cell.font=cf(); cell.border=bdr()
            cell.alignment=lft(); cell.fill=fill("FFF0FFF4")
        ws2.row_dimensions[idx].height=18
    col_widths(ws2,[30,22,50,12,22])

    # ── Sheet 3: Failed ───────────────────────────────────────────────────────
    ws3 = wb.create_sheet("Failed Tests")
    set_header(ws3, ["Test ID","Module","Test Name","Failure Reason","Duration(s)","Screenshot"], bg=FAI)
    failed = [r for r in results if r.get("status")=="FAIL"]
    for idx,r in enumerate(failed,2):
        vals=[r.get("test_id",""),r.get("module",""),r.get("name",""),
              r.get("failure_reason","")[:300],r.get("duration",0),r.get("screenshot","")]
        for c,v in enumerate(vals,1):
            cell=ws3.cell(idx,c,v); cell.font=cf(); cell.border=bdr()
            cell.alignment=lft(); cell.fill=fill("FFFFF5F5")
        ws3.row_dimensions[idx].height=22
    col_widths(ws3,[30,22,50,60,12,40])

    # ── Sheet 4: Skipped ──────────────────────────────────────────────────────
    ws4 = wb.create_sheet("Skipped Tests")
    set_header(ws4, ["Test ID","Module","Test Name","Reason"], bg=SKP)
    skipped = [r for r in results if r.get("status") not in ("PASS","FAIL")]
    for idx,r in enumerate(skipped,2):
        vals=[r.get("test_id",""),r.get("module",""),r.get("name",""),r.get("failure_reason","")]
        for c,v in enumerate(vals,1):
            cell=ws4.cell(idx,c,v); cell.font=cf(); cell.border=bdr()
            cell.alignment=lft(); cell.fill=fill("FFFFFFE0")
        ws4.row_dimensions[idx].height=18
    col_widths(ws4,[30,22,50,60])

    # ── Sheet 5: Execution Metrics ────────────────────────────────────────────
    ws5 = wb.create_sheet("Execution Metrics")
    total=len(results); pct=f"{len(passed)/total*100:.1f}%" if total else "0%"
    metrics = [
        ("Execution Date",      datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("Deployment URL",      BASE_URL),
        ("Total Tests",         total),
        ("Passed",              len(passed)),
        ("Failed",              len(failed)),
        ("Skipped",             len(skipped)),
        ("Pass Rate",           pct),
        ("Total Duration (s)",  round(sum(r.get("duration",0) for r in results),2)),
        ("Avg Duration (s)",    round(sum(r.get("duration",0) for r in results)/max(total,1),2)),
        ("Browser",             "Chrome (Headless)"),
        ("Framework",           "Selenium WebDriver + pytest"),
        ("Report Generated",    datetime.now().isoformat()),
    ]
    set_header(ws5, ["Metric","Value"])
    for idx,(k,v) in enumerate(metrics,2):
        ws5.cell(idx,1,k).font=Font(name="Calibri",sz=10,bold=True,color=DK)
        ws5.cell(idx,2,v).font=Font(name="Calibri",sz=10,color=DK)
        for c in [1,2]:
            ws5.cell(idx,c).border=bdr(); ws5.cell(idx,c).alignment=lft()
            ws5.cell(idx,c).fill=fill(GR if idx%2==0 else WH)
    col_widths(ws5,[30,50])

    # ── Sheet 6: Defect Summary ───────────────────────────────────────────────
    ws6 = wb.create_sheet("Defect Summary")
    set_header(ws6,["Defect ID","Test ID","Module","Defect Title","Severity","Status","Screenshot"],bg=FAI)
    for idx,r in enumerate([r for r in results if r.get("status")=="FAIL"],2):
        vals=[f"DEF-{idx-1:03d}",r.get("test_id",""),r.get("module",""),
              r.get("name",""),"Medium","Open",r.get("screenshot","")]
        for c,v in enumerate(vals,1):
            cell=ws6.cell(idx,c,v); cell.font=cf(); cell.border=bdr()
            cell.alignment=lft(); cell.fill=fill("FFFFF5F5")
        ws6.row_dimensions[idx].height=18
    col_widths(ws6,[14,30,22,50,12,12,40])

    out = EXCEL_DIR / "Automation_Test_Report.xlsx"
    try:
        wb.save(str(out))
        print(f"✓ Main report saved: {out} ({out.stat().st_size:,} bytes)")
    except Exception as e:
        print(f"✗ FAILED to save {out}: {e}", file=sys.stderr)
        raise

    # ── Separate workbooks ────────────────────────────────────────────────────
    def mini_wb(rows, title, path, bg):
        w=openpyxl.Workbook(); s=w.active; s.title=title
        set_header(s,["Test ID","Module","Test Name","Status","Duration","Failure"],bg=bg)
        for i,r in enumerate(rows,2):
            for c,v in enumerate([r.get("test_id",""),r.get("module",""),r.get("name",""),
                                   r.get("status",""),r.get("duration",0),
                                   r.get("failure_reason","")[:200]],1):
                s.cell(i,c,v).font=cf(); s.cell(i,c).border=bdr(); s.cell(i,c).alignment=lft()
            s.row_dimensions[i].height=18
        col_widths(s,[30,22,50,10,12,60])
        file_path = EXCEL_DIR/path
        try:
            w.save(str(file_path))
            print(f"✓ {path} saved ({file_path.stat().st_size:,} bytes)")
        except Exception as e:
            print(f"✗ FAILED to save {path}: {e}", file=sys.stderr)
            raise

    mini_wb(passed,  "Passed Tests",  "Passed_Test_Cases.xlsx",  PAS)
    mini_wb(failed,  "Failed Tests",  "Failed_Test_Cases.xlsx",  FAI)

    # Summary workbook
    sw=openpyxl.Workbook(); ss=sw.active; ss.title="Summary"
    set_header(ss,["Category","Total","Pass","Fail","Pass Rate"])
    cats={}
    for r in results:
        m=r.get("module","unknown"); cats.setdefault(m,{"p":0,"f":0})
        if r.get("status")=="PASS": cats[m]["p"]+=1
        else: cats[m]["f"]+=1
    for i,(m,d) in enumerate(sorted(cats.items()),2):
        t=d["p"]+d["f"]; p=f"{d['p']/t*100:.0f}%" if t else "0%"
        for c,v in enumerate([m,t,d["p"],d["f"],p],1):
            ss.cell(i,c,v).font=cf(); ss.cell(i,c).border=bdr()
            ss.cell(i,c).alignment=cen()
        ss.row_dimensions[i].height=18
    col_widths(ss,[25,10,10,10,12])
    summary_path = EXCEL_DIR/"Summary_Report.xlsx"
    try:
        sw.save(str(summary_path))
        print(f"✓ Summary_Report.xlsx saved ({summary_path.stat().st_size:,} bytes)")
    except Exception as e:
        print(f"✗ FAILED to save Summary_Report.xlsx: {e}", file=sys.stderr)
        raise

    return out
