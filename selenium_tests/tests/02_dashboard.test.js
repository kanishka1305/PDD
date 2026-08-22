'use strict';
const { By } = require('selenium-webdriver');
const { expect } = require('chai');
const { buildDriver } = require('../helpers/driver');
const cfg   = require('../helpers/config');
const utils = require('../helpers/utils');
const auth  = require('../helpers/auth');

const SUITE = '02 Dashboard';

describe(SUITE, function () {
  this.timeout(60000);
  let driver;

  before(async () => {
    driver = await buildDriver(true);
    await auth.ensureAccount(driver);
    await auth.login(driver);
    await utils.goto(driver, cfg.BASE_URL + '/dashboard');
    await driver.sleep(1500);
  });

  after(async () => {
    utils.saveResults();
    if (driver) await driver.quit();
  });

  it('TC-007 · Dashboard page title is correct', async () => {
    const t0 = Date.now();
    try {
      const title = await driver.getTitle();
      expect(title).to.include('DentAI');
      const ss = await utils.screenshot(driver, 'TC007_dashboard_title');
      utils.record(SUITE, 'TC-007 Dashboard page title', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC007_FAIL');
      utils.record(SUITE, 'TC-007 Dashboard page title', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-008 · Sidebar is visible with navigation links', async () => {
    const t0 = Date.now();
    try {
      const sidebar = await utils.exists(driver, By.css('.sidebar'));
      const navLinks = await driver.findElements(By.css('.sidebar nav a'));
      expect(sidebar).to.be.true;
      expect(navLinks.length).to.be.at.least(4);
      const ss = await utils.screenshot(driver, 'TC008_sidebar');
      utils.record(SUITE, 'TC-008 Sidebar visible with nav links', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC008_FAIL');
      utils.record(SUITE, 'TC-008 Sidebar visible with nav links', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-009 · KPI stat cards are rendered', async () => {
    const t0 = Date.now();
    try {
      const cards = await driver.findElements(By.css('.stat-card-dash, .stat-card'));
      expect(cards.length).to.be.at.least(1);
      const ss = await utils.screenshot(driver, 'TC009_kpi_cards');
      utils.record(SUITE, 'TC-009 KPI stat cards rendered', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC009_FAIL');
      utils.record(SUITE, 'TC-009 KPI stat cards rendered', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-010 · Quick action buttons are present', async () => {
    const t0 = Date.now();
    try {
      const btns = await driver.findElements(By.css('.qa-card, .btn-sm, .btn-outline'));
      expect(btns.length).to.be.at.least(2);
      const ss = await utils.screenshot(driver, 'TC010_quick_actions');
      utils.record(SUITE, 'TC-010 Quick action buttons present', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC010_FAIL');
      utils.record(SUITE, 'TC-010 Quick action buttons present', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-011 · Upload Scan nav link navigates correctly', async () => {
    const t0 = Date.now();
    try {
      const link = await driver.findElement(By.xpath("//a[contains(@href,'/upload')]"));
      await driver.executeScript('arguments[0].click();', link);
      await driver.sleep(1500);
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/upload');
      const ss = await utils.screenshot(driver, 'TC011_nav_upload');
      utils.record(SUITE, 'TC-011 Upload nav link works', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC011_FAIL');
      utils.record(SUITE, 'TC-011 Upload nav link works', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-012 · History nav link navigates correctly', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/dashboard');
      await driver.sleep(800);
      const link = await driver.findElement(By.xpath("//a[contains(@href,'/history')]"));
      await driver.executeScript('arguments[0].click();', link);
      await driver.sleep(1500);
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/history');
      const ss = await utils.screenshot(driver, 'TC012_nav_history');
      utils.record(SUITE, 'TC-012 History nav link works', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC012_FAIL');
      utils.record(SUITE, 'TC-012 History nav link works', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-013 · DentAI brand logo is visible', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/dashboard');
      await driver.sleep(800);
      const brand = await utils.exists(driver, By.css('.brand-text, .brand'));
      expect(brand).to.be.true;
      const ss = await utils.screenshot(driver, 'TC013_brand');
      utils.record(SUITE, 'TC-013 Brand logo visible', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC013_FAIL');
      utils.record(SUITE, 'TC-013 Brand logo visible', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-014 · User avatar/name displayed in sidebar', async () => {
    const t0 = Date.now();
    try {
      const avatar = await utils.exists(driver, By.css('.user-avatar, .user-info'));
      expect(avatar).to.be.true;
      const ss = await utils.screenshot(driver, 'TC014_user_info');
      utils.record(SUITE, 'TC-014 User info in sidebar', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC014_FAIL');
      utils.record(SUITE, 'TC-014 User info in sidebar', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });
});
