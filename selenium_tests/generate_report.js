'use strict';
/**
 * DentAI Selenium E2E — Excel Report Generator
 * Reads reports/test_results.json → writes reports/DentAI_E2E_Report.xlsx
 */
const ExcelJS = require('exceljs');
const path    = require('path');
const fs      = require('fs');

const RESULTS_FILE = path.join(__dirname, 'reports', 'test_results.json');
const OUTPUT_FILE  = path.join(__dirname, 'reports', 'DentAI_E2E_Report.xlsx');

/* ── Palette ── */
const C = {
  blueDark:   '1E3A5F', blueMed:  '2563EB', blueLight: 'DBEAFE',
  cyan:       '0EA5E9', teal:     '0D9488',
  green:      '16A34A', greenLt:  'DCFCE7',
  red:        'DC2626', redLt:    'FEE2E2',
  amber:      'D97706', amberLt:  'FEF3C7',
  purple:     '7C3AED', purpleLt: 'EDE9FE',
  white:      'FFFFFF', greyLt:   'F1F5F9',
  greyMed:    'E2E8F0', dark:     '0F172A',
};

const fill  = hex => ({ type:'pattern', pattern:'solid', fgColor:{argb:'FF'+hex} });
const font  = (sz=10, bold=false, color=C.dark) => ({ name:'Calibri', size:sz, bold, color:{argb:'FF'+color} });
const align = (h='center', v='middle', wrap=false) => ({ horizontal:h, vertical:v, wrapText:wrap });
const bdr   = (style='thin', color=C.greyMed) => {
  const s = { style, color:{argb:'FF'+color} };
  return { top:s, bottom:s, left:s, right:s };
};
const col = (ws, idx, width) => { ws.getColumn(idx).width = width; };

/* ── Status styling ── */
function statusStyle(status) {
  if (status === 'PASS') return { fill: fill(C.greenLt),  fontColor: C.green,  label: '✓  PASS'  };
  if (status === 'FAIL') return { fill: fill(C.redLt),    fontColor: C.red,    label: '✗  FAIL'  };
  if (status === 'SKIP') return { fill: fill(C.amberLt),  fontColor: C.amber,  label: '⊘  SKIP'  };
  if (status === 'WARN') return { fill: fill(C.purpleLt), fontColor: C.purple, label: '⚠  WARN'  };
  return   { fill: fill(C.greyLt),   fontColor: C.dark,   label: status };
}

function durationLabel(ms) {
  if (ms < 1000)  return ms + ' ms';
  return (ms / 1000).toFixed(1) + ' s';
}

/* ══════════════════════════════════════════════
   SHEET 1 — COVER
══════════════════════════════════════════════ */
function writeCover(wb, summary) {
  const ws = wb.addWorksheet('Cover');
  ws.views = [{ showGridLines: false }];

  // Banner rows
  for (let r = 1; r <= 9; r++) {
    ws.getRow(r).height = r <= 2 ? 10 : r === 3 ? 42 : r === 4 ? 28 : 18;
    for (let c = 1; c <= 14; c++) ws.getCell(r, c).fill = fill(C.blueDark);
  }

  // Title
  ws.mergeCells('B3:N3');
  const title = ws.getCell('B3');
  title.value     = 'DentAI  —  Selenium End-to-End Test Report';
  title.font      = font(26, true, C.white);
  title.alignment = align('left', 'middle');

  ws.mergeCells('B4:N4');
  const sub = ws.getCell('B4');
  sub.value     = 'CBCT AI Segmentation Platform  ·  Full Application E2E Coverage';
  sub.font      = font(13, false, C.cyan);
  sub.alignment = align('left', 'middle');

  ws.mergeCells('B5:N5');
  const meta = ws.getCell('B5');
  meta.value     = `Generated: ${summary.generatedAt}   ·   Environment: http://localhost:8000   ·   Browser: Chrome (headless)`;
  meta.font      = font(9, false, 'A0AEC0');
  meta.alignment = align('left', 'middle');

  // Summary KPI boxes
  const kpis = [
    { label:'Total Tests',    value: summary.total,          bg: C.blueLight,  accent: C.blueMed  },
    { label:'Passed',         value: summary.passed,         bg: C.greenLt,    accent: C.green    },
    { label:'Failed',         value: summary.failed,         bg: C.redLt,      accent: C.red      },
    { label:'Skipped/Warned', value: summary.skipped,        bg: C.amberLt,    accent: C.amber    },
    { label:'Pass Rate',      value: summary.passRate + '%', bg: C.purpleLt,   accent: C.purple   },
    { label:'Total Duration', value: summary.totalDuration,  bg: C.greyLt,     accent: C.blueDark },
  ];

  kpis.forEach((kpi, i) => {
    const startCol = 2 + i * 2;
    const labelRow = 11, valueRow = 12;
    ws.mergeCells(labelRow, startCol, labelRow, startCol + 1);
    ws.mergeCells(valueRow, startCol, valueRow + 2, startCol + 1);
    const lc = ws.getCell(labelRow, startCol);
    lc.value     = kpi.label;
    lc.font      = font(9, true, kpi.accent);
    lc.fill      = fill(kpi.bg);
    lc.alignment = align('center', 'middle');
    lc.border    = bdr();
    const vc = ws.getCell(valueRow, startCol);
    vc.value     = kpi.value;
    vc.font      = font(22, true, kpi.accent);
    vc.fill      = fill(kpi.bg);
    vc.alignment = align('center', 'middle');
    vc.border    = bdr();
    ws.getRow(labelRow).height  = 20;
    ws.getRow(valueRow).height  = 40;
    ws.getRow(valueRow+1).height = 40;
    ws.getRow(valueRow+2).height = 40;
  });

  // Suite breakdown table
  const tRow = 17;
  ws.mergeCells(tRow, 2, tRow, 8);
  const th = ws.getCell(tRow, 2);
  th.value     = 'TEST SUITE BREAKDOWN';
  th.font      = font(11, true, C.white);
  th.fill      = fill(C.blueMed);
  th.alignment = align('left', 'middle');
  ws.getRow(tRow).height = 22;

  const hRow = tRow + 1;
  ['Suite Name', 'Tests', 'Pass', 'Fail', 'Skip/Warn', 'Pass Rate', 'Duration'].forEach((h, i) => {
    const c = ws.getCell(hRow, 2 + i);
    c.value     = h;
    c.font      = font(9, true, C.white);
    c.fill      = fill(C.blueDark);
    c.alignment = align('center', 'middle');
    c.border    = bdr();
    ws.getColumn(2 + i).width = [32, 8, 8, 8, 12, 10, 12][i];
  });
  ws.getRow(hRow).height = 18;

  summary.suites.forEach((s, idx) => {
    const r = hRow + 1 + idx;
    const rowFill = idx % 2 === 0 ? fill(C.greyLt) : fill(C.white);
    const rate = s.total > 0 ? ((s.passed / s.total) * 100).toFixed(0) + '%' : '—';
    const vals = [s.name, s.total, s.passed, s.failed, s.skipped, rate, durationLabel(s.duration)];
    vals.forEach((v, ci) => {
      const c = ws.getCell(r, 2 + ci);
      c.value     = v;
      c.font      = font(9, false, C.dark);
      c.fill      = ci === 3 && s.failed > 0 ? fill(C.redLt) : ci === 2 ? fill(C.greenLt) : rowFill;
      c.alignment = align(ci === 0 ? 'left' : 'center', 'middle');
      c.border    = bdr();
    });
    ws.getRow(r).height = 16;
  });

  // Verdict
  const verdictRow = hRow + 1 + summary.suites.length + 2;
  ws.mergeCells(verdictRow, 2, verdictRow, 8);
  const vc2 = ws.getCell(verdictRow, 2);
  const isPass = summary.failed === 0;
  vc2.value     = isPass
    ? `✓  OVERALL VERDICT: PASS  —  All ${summary.total} tests passed with 0 failures`
    : `✗  OVERALL VERDICT: FAIL  —  ${summary.failed} test(s) failed out of ${summary.total}`;
  vc2.font      = font(12, true, isPass ? C.green : C.red);
  vc2.fill      = fill(isPass ? C.greenLt : C.redLt);
  vc2.alignment = align('center', 'middle');
  vc2.border    = bdr('medium', isPass ? C.green : C.red);
  ws.getRow(verdictRow).height = 26;
}

/* ══════════════════════════════════════════════
   SHEET 2 — ALL TEST CASES
══════════════════════════════════════════════ */
function writeAllTests(wb, results) {
  const ws = wb.addWorksheet('All Test Cases');
  ws.views = [{ showGridLines: false, state: 'frozen', xSplit: 0, ySplit: 2 }];

  // Header banner
  ws.mergeCells('A1:K1');
  const banner = ws.getCell('A1');
  banner.value     = 'DentAI — All E2E Test Cases  (' + results.length + ' total)';
  banner.font      = font(14, true, C.white);
  banner.fill      = fill(C.blueMed);
  banner.alignment = align('center', 'middle');
  ws.getRow(1).height = 28;

  // Column headers
  const headers = ['#', 'Suite', 'Test Case Name', 'Status', 'Duration', 'Timestamp', 'Error Detail', 'Screenshot'];
  const widths  = [5,   28,      42,               12,       11,         20,           48,             18];
  headers.forEach((h, i) => {
    const c = ws.getCell(2, i + 1);
    c.value     = h;
    c.font      = font(10, true, C.white);
    c.fill      = fill(C.blueDark);
    c.alignment = align('center', 'middle');
    c.border    = bdr();
    ws.getColumn(i + 1).width = widths[i];
  });
  ws.getRow(2).height = 22;

  // Data rows
  results.forEach((r, idx) => {
    const rowNum = idx + 3;
    const s      = statusStyle(r.status);
    const rowFill = idx % 2 === 0 ? fill(C.greyLt) : fill(C.white);

    const vals = [
      idx + 1,
      r.suite,
      r.name,
      s.label,
      durationLabel(r.duration),
      r.timestamp ? new Date(r.timestamp).toLocaleString('en-GB') : '—',
      r.error || '',
      r.screenshot ? path.basename(r.screenshot) : '',
    ];

    vals.forEach((v, ci) => {
      const cell = ws.getCell(rowNum, ci + 1);
      cell.value     = v;
      cell.border    = bdr();
      cell.alignment = align(ci === 2 || ci === 6 ? 'left' : 'center', 'middle', ci === 6);

      if (ci === 3) {
        cell.font = font(9, true, s.fontColor);
        cell.fill = s.fill;
      } else if (ci === 6 && r.error) {
        cell.font = font(8, false, C.red);
        cell.fill = fill(C.redLt);
      } else {
        cell.font = font(9, false, C.dark);
        cell.fill = rowFill;
      }
    });
    ws.getRow(rowNum).height = r.error ? 28 : 16;
  });
}

/* ══════════════════════════════════════════════
   SHEET 3 — SUITE SUMMARY
══════════════════════════════════════════════ */
function writeSuiteSummary(wb, summary) {
  const ws = wb.addWorksheet('Suite Summary');
  ws.views = [{ showGridLines: false }];

  ws.mergeCells('A1:H1');
  const b = ws.getCell('A1');
  b.value     = 'DentAI — Test Suite Summary';
  b.font      = font(14, true, C.white);
  b.fill      = fill(C.blueDark);
  b.alignment = align('center', 'middle');
  ws.getRow(1).height = 28;

  // Headers
  const hdrs = ['Suite', 'Total', 'Passed', 'Failed', 'Skipped', 'Pass %', 'Duration', 'Verdict'];
  const wids = [35, 8, 8, 8, 8, 10, 14, 16];
  hdrs.forEach((h, i) => {
    const c = ws.getCell(2, i + 1);
    c.value     = h;
    c.font      = font(10, true, C.white);
    c.fill      = fill(C.blueMed);
    c.alignment = align('center', 'middle');
    c.border    = bdr();
    ws.getColumn(i + 1).width = wids[i];
  });
  ws.getRow(2).height = 20;

  summary.suites.forEach((s, idx) => {
    const r       = idx + 3;
    const rate    = s.total > 0 ? ((s.passed / s.total) * 100).toFixed(1) : '0.0';
    const verdict = s.failed === 0 ? '✓ PASS' : '✗ FAIL';
    const vStyle  = s.failed === 0
      ? { fill: fill(C.greenLt), color: C.green }
      : { fill: fill(C.redLt),   color: C.red   };
    const rowFill = idx % 2 === 0 ? fill(C.greyLt) : fill(C.white);

    const vals = [s.name, s.total, s.passed, s.failed, s.skipped, rate + '%', durationLabel(s.duration), verdict];
    vals.forEach((v, ci) => {
      const cell = ws.getCell(r, ci + 1);
      cell.value     = v;
      cell.border    = bdr();
      cell.alignment = align(ci === 0 ? 'left' : 'center', 'middle');
      if (ci === 7) {
        cell.font = font(9, true, vStyle.color);
        cell.fill = vStyle.fill;
      } else if (ci === 3 && s.failed > 0) {
        cell.font = font(9, true, C.red);
        cell.fill = fill(C.redLt);
      } else if (ci === 2) {
        cell.font = font(9, true, C.green);
        cell.fill = fill(C.greenLt);
      } else {
        cell.font = font(9, false, C.dark);
        cell.fill = rowFill;
      }
    });
    ws.getRow(r).height = 18;
  });
}

/* ══════════════════════════════════════════════
   SHEET 4 — FAILED TESTS (if any)
══════════════════════════════════════════════ */
function writeFailedTests(wb, results) {
  const failed = results.filter(r => r.status === 'FAIL');
  const ws = wb.addWorksheet('Failed Tests');
  ws.views = [{ showGridLines: false }];

  ws.mergeCells('A1:F1');
  const b = ws.getCell('A1');
  b.value     = failed.length === 0
    ? '✓  No Failures — All tests passed!'
    : `✗  Failed Tests  (${failed.length} failures)`;
  b.font      = font(14, true, C.white);
  b.fill      = fill(failed.length === 0 ? C.green : C.red);
  b.alignment = align('center', 'middle');
  ws.getRow(1).height = 28;

  if (failed.length === 0) {
    ws.mergeCells('A3:F3');
    const ok = ws.getCell('A3');
    ok.value     = '🎉  Excellent! Every single test case passed with zero failures.';
    ok.font      = font(13, true, C.green);
    ok.fill      = fill(C.greenLt);
    ok.alignment = align('center', 'middle');
    ws.getRow(3).height = 32;
    for (let c = 1; c <= 6; c++) ws.getColumn(c).width = 20;
    return;
  }

  const hdrs = ['Suite', 'Test Case', 'Duration', 'Error Message', 'Screenshot', 'Timestamp'];
  const wids = [28, 40, 10, 55, 22, 22];
  hdrs.forEach((h, i) => {
    const c = ws.getCell(2, i + 1);
    c.value = h; c.font = font(10, true, C.white);
    c.fill  = fill(C.red); c.alignment = align('center', 'middle');
    c.border = bdr(); ws.getColumn(i + 1).width = wids[i];
  });
  ws.getRow(2).height = 20;

  failed.forEach((r, idx) => {
    const row = idx + 3;
    const vals = [
      r.suite, r.name, durationLabel(r.duration),
      r.error || 'Unknown error',
      r.screenshot ? path.basename(r.screenshot) : '—',
      r.timestamp ? new Date(r.timestamp).toLocaleString('en-GB') : '—',
    ];
    vals.forEach((v, ci) => {
      const cell = ws.getCell(row, ci + 1);
      cell.value     = v;
      cell.font      = font(9, false, ci === 3 ? C.red : C.dark);
      cell.fill      = fill(idx % 2 === 0 ? C.redLt : C.white);
      cell.alignment = align(ci > 1 ? 'center' : 'left', 'middle', ci === 3);
      cell.border    = bdr();
    });
    ws.getRow(row).height = 20;
  });
}

/* ══════════════════════════════════════════════
   SHEET 5 — PERFORMANCE ANALYSIS
══════════════════════════════════════════════ */
function writePerformance(wb, results) {
  const ws = wb.addWorksheet('Performance');
  ws.views = [{ showGridLines: false }];

  ws.mergeCells('A1:G1');
  const b = ws.getCell('A1');
  b.value     = 'DentAI — Test Execution Performance Analysis';
  b.font      = font(14, true, C.white);
  b.fill      = fill(C.teal);
  b.alignment = align('center', 'middle');
  ws.getRow(1).height = 28;

  const hdrs = ['Test Case', 'Suite', 'Duration (ms)', 'Duration', 'Status', 'Speed Rating', 'Remarks'];
  const wids = [44, 28, 14, 12, 12, 14, 24];
  hdrs.forEach((h, i) => {
    const c = ws.getCell(2, i + 1);
    c.value = h; c.font = font(10, true, C.white);
    c.fill  = fill(C.teal); c.alignment = align('center', 'middle');
    c.border = bdr(); ws.getColumn(i + 1).width = wids[i];
  });
  ws.getRow(2).height = 20;

  // Sort by duration descending
  const sorted = [...results].sort((a, b) => b.duration - a.duration);

  sorted.forEach((r, idx) => {
    const row   = idx + 3;
    const ms    = r.duration;
    let speed, speedColor, remark;
    if (ms < 500)       { speed = '⚡ Fast';   speedColor = C.green;  remark = 'Excellent response'; }
    else if (ms < 2000) { speed = '✓ Normal';  speedColor = C.blueMed; remark = 'Acceptable'; }
    else if (ms < 5000) { speed = '⚠ Slow';   speedColor = C.amber;  remark = 'May need optimisation'; }
    else                { speed = '✗ Critical';speedColor = C.red;    remark = 'Investigate performance'; }

    const vals = [r.name, r.suite, ms, durationLabel(ms), statusStyle(r.status).label, speed, remark];
    vals.forEach((v, ci) => {
      const cell = ws.getCell(row, ci + 1);
      cell.value     = v;
      cell.alignment = align(ci <= 1 || ci === 6 ? 'left' : 'center', 'middle');
      cell.border    = bdr();
      const rowFill  = idx % 2 === 0 ? fill(C.greyLt) : fill(C.white);
      if (ci === 4) { cell.font = font(9, true, statusStyle(r.status).fontColor); cell.fill = statusStyle(r.status).fill; }
      else if (ci === 5) { cell.font = font(9, true, speedColor); cell.fill = rowFill; }
      else { cell.font = font(9, false, C.dark); cell.fill = rowFill; }
    });
    ws.getRow(row).height = 16;
  });

  // Stats summary
  const durs    = results.map(r => r.duration);
  const avgDur  = Math.round(durs.reduce((a,b) => a+b, 0) / (durs.length || 1));
  const minDur  = Math.min(...durs);
  const maxDur  = Math.max(...durs);
  const p95     = durs.sort((a,b) => a-b)[Math.floor(durs.length * 0.95)] || 0;

  const statsRow = results.length + 4;
  [
    ['Average Duration', durationLabel(avgDur)],
    ['Fastest Test',     durationLabel(minDur)],
    ['Slowest Test',     durationLabel(maxDur)],
    ['95th Percentile',  durationLabel(p95)],
  ].forEach(([label, val], i) => {
    const r = statsRow + i;
    const lc = ws.getCell(r, 1);
    lc.value = label; lc.font = font(9, true, C.teal);
    lc.fill  = fill(C.greyLt); lc.alignment = align('left', 'middle'); lc.border = bdr();
    const vc = ws.getCell(r, 2);
    vc.value = val; vc.font = font(9, false, C.dark);
    vc.fill  = fill(C.greyLt); vc.alignment = align('center', 'middle'); vc.border = bdr();
    ws.getRow(r).height = 16;
  });
}

/* ══════════════════════════════════════════════
   MAIN — Build summary and write workbook
══════════════════════════════════════════════ */
function buildSummary(results) {
  const suiteMap = {};
  results.forEach(r => {
    if (!suiteMap[r.suite]) suiteMap[r.suite] = { name:r.suite, total:0, passed:0, failed:0, skipped:0, duration:0 };
    const s = suiteMap[r.suite];
    s.total++;
    s.duration += r.duration;
    if (r.status === 'PASS')           s.passed++;
    else if (r.status === 'FAIL')      s.failed++;
    else                               s.skipped++;
  });

  const total    = results.length;
  const passed   = results.filter(r => r.status === 'PASS').length;
  const failed   = results.filter(r => r.status === 'FAIL').length;
  const skipped  = total - passed - failed;
  const totalMs  = results.reduce((a,r) => a + r.duration, 0);
  const passRate = total > 0 ? ((passed / total) * 100).toFixed(1) : '0.0';

  return {
    total, passed, failed, skipped,
    passRate,
    totalDuration: durationLabel(totalMs),
    generatedAt: new Date().toLocaleString('en-GB', { dateStyle:'full', timeStyle:'medium' }),
    suites: Object.values(suiteMap),
  };
}

async function generateReport() {
  // Load results
  if (!fs.existsSync(RESULTS_FILE)) {
    console.error('ERROR: test_results.json not found at', RESULTS_FILE);
    console.error('Run "npm test" first to generate results.');
    process.exit(1);
  }

  const results = JSON.parse(fs.readFileSync(RESULTS_FILE, 'utf8'));
  const summary = buildSummary(results);

  console.log(`\n📊 Building Excel report...`);
  console.log(`   Total:  ${summary.total} tests`);
  console.log(`   Passed: ${summary.passed}`);
  console.log(`   Failed: ${summary.failed}`);
  console.log(`   Pass Rate: ${summary.passRate}%`);

  const wb = new ExcelJS.Workbook();
  wb.creator    = 'DentAI Selenium Suite';
  wb.created    = new Date();
  wb.properties.date1904 = false;

  writeCover(wb, summary);
  writeAllTests(wb, results);
  writeSuiteSummary(wb, summary);
  writeFailedTests(wb, results);
  writePerformance(wb, results);

  // Ensure output dir exists
  const outDir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  await wb.xlsx.writeFile(OUTPUT_FILE);

  console.log(`\n✅ Excel report saved to:\n   ${OUTPUT_FILE}\n`);
  return OUTPUT_FILE;
}

generateReport().catch(err => {
  console.error('Report generation failed:', err.message);
  process.exit(1);
});
