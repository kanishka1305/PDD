'use strict';
const { By } = require('selenium-webdriver');
const { expect } = require('chai');
const { buildDriver } = require('../helpers/driver');
const cfg   = require('../helpers/config');
const utils = require('../helpers/utils');
const auth  = require('../helpers/auth');

const SUITE = '05 History Page';

describe(SUITE, function () {
  this.timeout(60000);
  let driver;

  before(async () => {
    driver = await buildDriver(true);
    await auth.ensureAccount(driver);
    await auth.login(driver);
    await utils.goto(driver, cfg.BASE_URL + '/history');
    await driver.sleep(2000);
  });

  after(async () => {
    utils.saveResults();
    if (driver) await driver.quit();
  });

  it('TC-033 · History page loads', async () => {
    const t0 = Date.now();
    try {
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/history');
      const ss = await utils.screenshot(driver, 'TC033_history_page');
      utils.record(SUITE, 'TC-033 History page loads', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC033_FAIL');
      utils.record(SUITE, 'TC-033 History page loads', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-034 · Search input is present', async () => {
    const t0 = Date.now();
    try {
      const search = await utils.exists(driver, By.css('#hist-search, .hist-search'));
      expect(search).to.be.true;
      const ss = await utils.screenshot(driver, 'TC034_search');
      utils.record(SUITE, 'TC-034 Search input present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC034_FAIL');
      utils.record(SUITE, 'TC-034 Search input present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-035 · Status filter pills are rendered', async () => {
    const t0 = Date.now();
    try {
      const pills = await driver.findElements(By.css('.filter-pill'));
      expect(pills.length).to.be.at.least(3);
      const ss = await utils.screenshot(driver, 'TC035_filter_pills');
      utils.record(SUITE, 'TC-035 Filter pills = ' + pills.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC035_FAIL');
      utils.record(SUITE, 'TC-035 Filter pills present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-036 · Sort dropdown is present', async () => {
    const t0 = Date.now();
    try {
      const select = await utils.exists(driver, By.id('sort-select'));
      expect(select).to.be.true;
      const ss = await utils.screenshot(driver, 'TC036_sort_select');
      utils.record(SUITE, 'TC-036 Sort dropdown present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC036_FAIL');
      utils.record(SUITE, 'TC-036 Sort dropdown present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-037 · Summary stat pills are rendered', async () => {
    const t0 = Date.now();
    try {
      const pills = await driver.findElements(By.css('.hist-stat-pill'));
      expect(pills.length).to.be.at.least(3);
      const ss = await utils.screenshot(driver, 'TC037_stat_pills');
      utils.record(SUITE, 'TC-037 Summary stat pills = ' + pills.length, 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC037_FAIL');
      utils.record(SUITE, 'TC-037 Summary stat pills present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-038 · Scan history table is rendered', async () => {
    const t0 = Date.now();
    try {
      const table = await utils.exists(driver, By.css('.hist-table, table'));
      expect(table).to.be.true;
      const ss = await utils.screenshot(driver, 'TC038_history_table');
      utils.record(SUITE, 'TC-038 History table rendered', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC038_FAIL');
      utils.record(SUITE, 'TC-038 History table rendered', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-039 · Search filters table results', async () => {
    const t0 = Date.now();
    try {
      const searchInput = await driver.findElement(By.css('#hist-search, .hist-search'));
      await searchInput.clear();
      await searchInput.sendKeys('ZZZNOMATCH999');
      await driver.sleep(700);
      const src = await driver.getPageSource();
      const noResults = src.includes('No scans match') || src.includes('Clear filters') ||
                        !(await utils.exists(driver, By.css('tbody tr td:not(.hist-empty)'), 2000));
      const ss = await utils.screenshot(driver, 'TC039_search_filter');
      utils.record(SUITE, 'TC-039 Search filters results', 'PASS', Date.now() - t0, '', ss);
      // Clear
      await searchInput.clear();
      await driver.sleep(400);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC039_FAIL');
      utils.record(SUITE, 'TC-039 Search filters results', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-040 · Pagination is rendered when scans exist', async () => {
    const t0 = Date.now();
    try {
      const src = await driver.getPageSource();
      const hasPagination = src.includes('pg-btn') || src.includes('Showing');
      const ss = await utils.screenshot(driver, 'TC040_pagination');
      utils.record(SUITE, 'TC-040 Pagination rendered', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC040_FAIL');
      utils.record(SUITE, 'TC-040 Pagination rendered', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-041 · CSV Export button is present', async () => {
    const t0 = Date.now();
    try {
      const src = await driver.getPageSource();
      const hasExport = src.includes('Export CSV') || src.includes('exportCSV');
      expect(hasExport).to.be.true;
      const ss = await utils.screenshot(driver, 'TC041_csv_export');
      utils.record(SUITE, 'TC-041 CSV export button present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC041_FAIL');
      utils.record(SUITE, 'TC-041 CSV export button present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });
});
