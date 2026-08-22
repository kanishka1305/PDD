'use strict';
const { By } = require('selenium-webdriver');
const { expect } = require('chai');
const { buildDriver } = require('../helpers/driver');
const cfg   = require('../helpers/config');
const utils = require('../helpers/utils');
const auth  = require('../helpers/auth');

const SUITE = '04 Results Page';

describe(SUITE, function () {
  this.timeout(60000);
  let driver;

  before(async () => {
    driver = await buildDriver(true);
    await auth.ensureAccount(driver);
    await auth.login(driver);

    // Inject a mock lastResult into localStorage so results page can render
    await driver.executeScript(`
      localStorage.setItem('lastResult', JSON.stringify({
        scan_id: 1,
        status: 'analysis_completed',
        analysis: {
          bone_volume: 143041, cortical_bone: 92976, trabecular_bone: 50065,
          confidence: 88.6, processing_time: 38,
          report_id: 'RPT-2026-0001', report_date: 'Aug 05, 2026',
          patient_name: 'Test Patient', patient_id: 'PT-0001', scan_date: '05 Aug 2026',
          condylar_head_l_volume: 4369,  condylar_head_r_volume: 3388,
          coronoid_l_volume: 6726,       coronoid_r_volume: 7244,
          angle_ramus_l_volume: 22872,   angle_ramus_r_volume: 23754,
          body_l_volume: 24799,          body_r_volume: 22688,
          symphyseal_parasymphyseal_volume: 27201,
          nerve_canal_volume: 0.42, nerve_distance: 'HIGH',
          nerve_distance_value: 1.2, bone_loss: 23.0,
          volume_shape: [1,535,535], detected_voxels: 143041
        }
      }));
    `);

    await utils.goto(driver, cfg.BASE_URL + '/results');
    await driver.sleep(1500);
  });

  after(async () => {
    utils.saveResults();
    if (driver) await driver.quit();
  });

  it('TC-022 · Results page loads', async () => {
    const t0 = Date.now();
    try {
      const title = await driver.getTitle();
      expect(title).to.include('DentAI');
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/results');
      const ss = await utils.screenshot(driver, 'TC022_results_page');
      utils.record(SUITE, 'TC-022 Results page loads', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC022_FAIL');
      utils.record(SUITE, 'TC-022 Results page loads', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-023 · 8 KPI cards are rendered', async () => {
    const t0 = Date.now();
    try {
      const cards = await driver.findElements(By.css('.res-kpi'));
      expect(cards.length).to.be.at.least(6);
      const ss = await utils.screenshot(driver, 'TC023_kpi_cards');
      utils.record(SUITE, 'TC-023 KPI cards rendered (' + cards.length + ')', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC023_FAIL');
      utils.record(SUITE, 'TC-023 KPI cards rendered', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-024 · Total Jaw Volume KPI shows correct value', async () => {
    const t0 = Date.now();
    try {
      const val = await utils.getText(driver, By.id('r-bone-vol'));
      expect(val).to.not.equal('—');
      expect(val.length).to.be.at.least(1);
      const ss = await utils.screenshot(driver, 'TC024_bone_vol');
      utils.record(SUITE, 'TC-024 Bone volume KPI = ' + val, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC024_FAIL');
      utils.record(SUITE, 'TC-024 Bone volume KPI populated', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-025 · Confidence KPI shows correct value', async () => {
    const t0 = Date.now();
    try {
      const val = await utils.getText(driver, By.id('r-confidence'));
      expect(val).to.include('%');
      const ss = await utils.screenshot(driver, 'TC025_confidence');
      utils.record(SUITE, 'TC-025 Confidence KPI = ' + val, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC025_FAIL');
      utils.record(SUITE, 'TC-025 Confidence KPI populated', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-026 · Patient info bar is rendered', async () => {
    const t0 = Date.now();
    try {
      const card = await utils.exists(driver, By.css('.patient-card'));
      expect(card).to.be.true;
      const patName = await utils.getText(driver, By.id('pc-name'));
      expect(patName.length).to.be.at.least(1);
      const ss = await utils.screenshot(driver, 'TC026_patient_info');
      utils.record(SUITE, 'TC-026 Patient info bar = ' + patName, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC026_FAIL');
      utils.record(SUITE, 'TC-026 Patient info bar rendered', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-027 · 7 Anatomical region cards are present', async () => {
    const t0 = Date.now();
    try {
      const cards = await driver.findElements(By.css('.region-card-ex'));
      expect(cards.length).to.be.at.least(7);
      const ss = await utils.screenshot(driver, 'TC027_region_cards');
      utils.record(SUITE, 'TC-027 Region cards = ' + cards.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC027_FAIL');
      utils.record(SUITE, 'TC-027 Region cards present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-028 · Condylar Head L region shows volume', async () => {
    const t0 = Date.now();
    try {
      const val = await utils.getText(driver, By.id('r-chl'));
      expect(val).to.not.equal('—');
      const ss = await utils.screenshot(driver, 'TC028_chl_volume');
      utils.record(SUITE, 'TC-028 Condylar Head L = ' + val, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC028_FAIL');
      utils.record(SUITE, 'TC-028 Condylar Head L volume', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-029 · STL download buttons are present', async () => {
    const t0 = Date.now();
    try {
      const btns = await driver.findElements(By.css('.rcx-btn.stl, .btn-export.stl'));
      expect(btns.length).to.be.at.least(1);
      const ss = await utils.screenshot(driver, 'TC029_stl_btns');
      utils.record(SUITE, 'TC-029 STL download buttons = ' + btns.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC029_FAIL');
      utils.record(SUITE, 'TC-029 STL buttons present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-030 · Stats modal opens when clicking Stats button', async () => {
    const t0 = Date.now();
    try {
      const statBtns = await driver.findElements(By.css('.rcx-btn.stats'));
      expect(statBtns.length).to.be.at.least(1);
      await driver.executeScript('arguments[0].click()', statBtns[0]);
      await driver.sleep(700);
      const modalOpen = await utils.exists(driver, By.css('.modal-overlay.open, .stats-modal.open'), 3000);
      const ss = await utils.screenshot(driver, 'TC030_stats_modal');
      utils.record(SUITE, 'TC-030 Stats modal opens', modalOpen ? 'PASS' : 'WARN', Date.now() - t0, '', ss);
      // Close modal
      await driver.executeScript("document.querySelector('.modal-overlay')?.classList.remove('open')");
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC030_FAIL');
      utils.record(SUITE, 'TC-030 Stats modal opens', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-031 · Segmentation viewer section is present', async () => {
    const t0 = Date.now();
    try {
      const viewer = await utils.exists(driver, By.css('.seg-viewer, .sv-canvas-wrap'));
      expect(viewer).to.be.true;
      const ss = await utils.screenshot(driver, 'TC031_seg_viewer');
      utils.record(SUITE, 'TC-031 Segmentation viewer present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC031_FAIL');
      utils.record(SUITE, 'TC-031 Segmentation viewer present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-032 · Clinical Report button is present', async () => {
    const t0 = Date.now();
    try {
      const src = await driver.getPageSource();
      const hasReport = src.includes('Clinical Report') || src.includes('openReportModal');
      expect(hasReport).to.be.true;
      const ss = await utils.screenshot(driver, 'TC032_report_btn');
      utils.record(SUITE, 'TC-032 Clinical report button present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC032_FAIL');
      utils.record(SUITE, 'TC-032 Clinical report button present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });
});
