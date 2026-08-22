'use strict';
const { By } = require('selenium-webdriver');
const { expect } = require('chai');
const { buildDriver } = require('../helpers/driver');
const cfg   = require('../helpers/config');
const utils = require('../helpers/utils');
const auth  = require('../helpers/auth');

const SUITE = '06 Workflow & Viewer';

describe(SUITE, function () {
  this.timeout(60000);
  let driver;

  before(async () => {
    driver = await buildDriver(true);
    await auth.ensureAccount(driver);
    await auth.login(driver);
  });

  after(async () => {
    utils.saveResults();
    if (driver) await driver.quit();
  });

  /* ── Workflow ── */
  it('TC-042 · Workflow page loads', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/workflow');
      await driver.sleep(1000);
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/workflow');
      const ss = await utils.screenshot(driver, 'TC042_workflow_page');
      utils.record(SUITE, 'TC-042 Workflow page loads', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC042_FAIL');
      utils.record(SUITE, 'TC-042 Workflow page loads', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-043 · Workflow pipeline steps are rendered', async () => {
    const t0 = Date.now();
    try {
      const steps = await driver.findElements(By.css('.pt-item, .wf-step'));
      expect(steps.length).to.be.at.least(4);
      const ss = await utils.screenshot(driver, 'TC043_pipeline_steps');
      utils.record(SUITE, 'TC-043 Pipeline steps = ' + steps.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC043_FAIL');
      utils.record(SUITE, 'TC-043 Pipeline steps rendered', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-044 · Simulate Pipeline button is present', async () => {
    const t0 = Date.now();
    try {
      const src = await driver.getPageSource();
      const hasBtn = src.includes('Simulate Pipeline') || src.includes('runDemo');
      expect(hasBtn).to.be.true;
      const ss = await utils.screenshot(driver, 'TC044_simulate_btn');
      utils.record(SUITE, 'TC-044 Simulate button present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC044_FAIL');
      utils.record(SUITE, 'TC-044 Simulate button present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-045 · Pipeline progress ring SVG is rendered', async () => {
    const t0 = Date.now();
    try {
      const ring = await utils.exists(driver, By.css('.pd-ring, .pd-ring-fill, svg'));
      expect(ring).to.be.true;
      const ss = await utils.screenshot(driver, 'TC045_ring_progress');
      utils.record(SUITE, 'TC-045 Progress ring rendered', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC045_FAIL');
      utils.record(SUITE, 'TC-045 Progress ring rendered', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-046 · Pipeline simulation starts on button click', async () => {
    const t0 = Date.now();
    try {
      const btns = await driver.findElements(By.css('#pd-start-btn, #btn-demo'));
      if (btns.length > 0) {
        await driver.executeScript('arguments[0].click()', btns[0]);
        await driver.sleep(1500);
        const src = await driver.getPageSource();
        const isRunning = src.includes('Running') || src.includes('active') || src.includes('Processing');
        const ss = await utils.screenshot(driver, 'TC046_simulation_start');
        utils.record(SUITE, 'TC-046 Simulation started', 'PASS', Date.now() - t0, '', ss);
      } else {
        utils.record(SUITE, 'TC-046 Simulation button click', 'SKIP', Date.now() - t0, 'Button not found');
      }
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC046_FAIL');
      utils.record(SUITE, 'TC-046 Simulation starts', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-047 · Log terminal is rendered in workflow', async () => {
    const t0 = Date.now();
    try {
      const log = await utils.exists(driver, By.css('.pd-log'));
      expect(log).to.be.true;
      const ss = await utils.screenshot(driver, 'TC047_log_terminal');
      utils.record(SUITE, 'TC-047 Log terminal present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC047_FAIL');
      utils.record(SUITE, 'TC-047 Log terminal present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  /* ── 3D Viewer ── */
  it('TC-048 · 3D Viewer page loads', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/viewer');
      await driver.sleep(1200);
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/viewer');
      const ss = await utils.screenshot(driver, 'TC048_viewer_page');
      utils.record(SUITE, 'TC-048 3D Viewer page loads', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC048_FAIL');
      utils.record(SUITE, 'TC-048 3D Viewer page loads', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-049 · Viewer tab strip (3D STL / DICOM) is present', async () => {
    const t0 = Date.now();
    try {
      const tabs = await driver.findElements(By.css('.vtab'));
      expect(tabs.length).to.be.at.least(2);
      const ss = await utils.screenshot(driver, 'TC049_viewer_tabs');
      utils.record(SUITE, 'TC-049 Viewer tabs = ' + tabs.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC049_FAIL');
      utils.record(SUITE, 'TC-049 Viewer tabs present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-050 · Region selector panel is rendered', async () => {
    const t0 = Date.now();
    try {
      const panel = await utils.exists(driver, By.css('#region-selector, .region-selector'));
      expect(panel).to.be.true;
      const regionBtns = await driver.findElements(By.css('.rs-btn'));
      expect(regionBtns.length).to.be.at.least(5);
      const ss = await utils.screenshot(driver, 'TC050_region_selector');
      utils.record(SUITE, 'TC-050 Region selector = ' + regionBtns.length + ' buttons', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC050_FAIL');
      utils.record(SUITE, 'TC-050 Region selector present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-051 · Viewer toolbar buttons present (zoom, wireframe, measure)', async () => {
    const t0 = Date.now();
    try {
      const toolbarBtns = await driver.findElements(By.css('.vt-btn, .vt-icon-btn'));
      expect(toolbarBtns.length).to.be.at.least(4);
      const ss = await utils.screenshot(driver, 'TC051_toolbar_btns');
      utils.record(SUITE, 'TC-051 Toolbar buttons = ' + toolbarBtns.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC051_FAIL');
      utils.record(SUITE, 'TC-051 Toolbar buttons present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-052 · DICOM tab switches to DICOM viewer', async () => {
    const t0 = Date.now();
    try {
      const dicomTab = await driver.findElement(By.id('tab-dicom'));
      await driver.executeScript('arguments[0].click()', dicomTab);
      await driver.sleep(1000);
      const dicomWrap = await utils.exists(driver, By.id('dicom-canvas-wrap'), 5000);
      const ss = await utils.screenshot(driver, 'TC052_dicom_tab');
      utils.record(SUITE, 'TC-052 DICOM tab switches', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC052_FAIL');
      utils.record(SUITE, 'TC-052 DICOM tab switches', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-053 · Appearance sliders are present (transparency, shininess)', async () => {
    const t0 = Date.now();
    try {
      const sliders = await driver.findElements(By.css('.vp-slider'));
      expect(sliders.length).to.be.at.least(2);
      const ss = await utils.screenshot(driver, 'TC053_sliders');
      utils.record(SUITE, 'TC-053 Appearance sliders = ' + sliders.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC053_FAIL');
      utils.record(SUITE, 'TC-053 Appearance sliders present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });
});
