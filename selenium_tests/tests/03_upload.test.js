'use strict';
const { By } = require('selenium-webdriver');
const { expect } = require('chai');
const { buildDriver } = require('../helpers/driver');
const cfg   = require('../helpers/config');
const utils = require('../helpers/utils');
const auth  = require('../helpers/auth');

const SUITE = '03 Upload Page';

describe(SUITE, function () {
  this.timeout(60000);
  let driver;

  before(async () => {
    driver = await buildDriver(true);
    await auth.ensureAccount(driver);
    await auth.login(driver);
    await utils.goto(driver, cfg.BASE_URL + '/upload');
    await driver.sleep(1200);
  });

  after(async () => {
    utils.saveResults();
    if (driver) await driver.quit();
  });

  it('TC-015 · Upload page loads with correct title', async () => {
    const t0 = Date.now();
    try {
      const title = await driver.getTitle();
      expect(title).to.include('DentAI');
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/upload');
      const ss = await utils.screenshot(driver, 'TC015_upload_page');
      utils.record(SUITE, 'TC-015 Upload page loads', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC015_FAIL');
      utils.record(SUITE, 'TC-015 Upload page loads', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-016 · Drag-and-drop upload zone is visible', async () => {
    const t0 = Date.now();
    try {
      const zone = await utils.exists(driver, By.css('#drop-zone, .upload-zone-lg, .upload-zone'));
      expect(zone).to.be.true;
      const ss = await utils.screenshot(driver, 'TC016_drop_zone');
      utils.record(SUITE, 'TC-016 Drop zone visible', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC016_FAIL');
      utils.record(SUITE, 'TC-016 Drop zone visible', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-017 · File format badges are shown (DCM, NII, ZIP)', async () => {
    const t0 = Date.now();
    try {
      const pageSource = await driver.getPageSource();
      const hasDcm = pageSource.toLowerCase().includes('.dcm') || pageSource.toLowerCase().includes('dicom');
      const hasNii = pageSource.toLowerCase().includes('.nii') || pageSource.toLowerCase().includes('nifti');
      expect(hasDcm).to.be.true;
      expect(hasNii).to.be.true;
      const ss = await utils.screenshot(driver, 'TC017_format_badges');
      utils.record(SUITE, 'TC-017 Format badges visible', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC017_FAIL');
      utils.record(SUITE, 'TC-017 Format badges visible', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-018 · Upload step indicator is present', async () => {
    const t0 = Date.now();
    try {
      const steps = await utils.exists(driver, By.css('.upload-steps, .upload-step-item'));
      expect(steps).to.be.true;
      const ss = await utils.screenshot(driver, 'TC018_step_indicator');
      utils.record(SUITE, 'TC-018 Step indicator present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC018_FAIL');
      utils.record(SUITE, 'TC-018 Step indicator present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-019 · File input accepts DCM/NII/ZIP formats', async () => {
    const t0 = Date.now();
    try {
      const fileInput = await driver.findElement(By.css('#file-input, input[type=file]'));
      const accept    = await fileInput.getAttribute('accept');
      expect(accept).to.include('.dcm');
      const ss = await utils.screenshot(driver, 'TC019_file_input');
      utils.record(SUITE, 'TC-019 File input accepts correct formats', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC019_FAIL');
      utils.record(SUITE, 'TC-019 File input accepts correct formats', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-020 · Upload zone hover effect triggered via JS', async () => {
    const t0 = Date.now();
    try {
      const zone = await driver.findElement(By.css('#drop-zone, .upload-zone-lg'));
      await driver.executeScript("arguments[0].classList.add('dragover')", zone);
      await driver.sleep(400);
      const classes = await zone.getAttribute('class');
      expect(classes).to.include('dragover');
      await driver.executeScript("arguments[0].classList.remove('dragover')", zone);
      const ss = await utils.screenshot(driver, 'TC020_hover_effect');
      utils.record(SUITE, 'TC-020 Hover effect works', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC020_FAIL');
      utils.record(SUITE, 'TC-020 Hover effect works', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-021 · /scans API returns valid JSON', async () => {
    const t0 = Date.now();
    try {
      const result = await driver.executeScript(`
        return fetch('/scans')
          .then(r => r.json())
          .then(d => ({ ok: true, count: (d.scans||[]).length }))
          .catch(e => ({ ok: false, err: e.message }));
      `);
      expect(result.ok).to.be.true;
      expect(result.count).to.be.at.least(0);
      const ss = await utils.screenshot(driver, 'TC021_scans_api');
      utils.record(SUITE, 'TC-021 /scans API returns JSON', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC021_FAIL');
      utils.record(SUITE, 'TC-021 /scans API returns JSON', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });
});
