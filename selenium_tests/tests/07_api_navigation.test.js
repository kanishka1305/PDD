'use strict';
const { By } = require('selenium-webdriver');
const { expect } = require('chai');
const { buildDriver } = require('../helpers/driver');
const cfg   = require('../helpers/config');
const utils = require('../helpers/utils');
const auth  = require('../helpers/auth');

const SUITE = '07 API & Navigation';

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

  it('TC-054 · /health API returns 200', async () => {
    const t0 = Date.now();
    try {
      const result = await driver.executeScript(`
        return fetch('/health').then(r => ({ status: r.status })).catch(e => ({ status: 0 }));
      `);
      expect(result.status).to.equal(200);
      utils.record(SUITE, 'TC-054 /health API returns 200', 'PASS', Date.now() - t0);
    } catch (e) {
      utils.record(SUITE, 'TC-054 /health API returns 200', 'FAIL', Date.now() - t0, e.message);
      throw e;
    }
  });

  it('TC-055 · /scans API returns scans array', async () => {
    const t0 = Date.now();
    try {
      const result = await driver.executeScript(`
        return fetch('/scans')
          .then(r => r.json())
          .then(d => ({ ok: Array.isArray(d.scans), count: d.scans.length }))
          .catch(() => ({ ok: false }));
      `);
      expect(result.ok).to.be.true;
      utils.record(SUITE, 'TC-055 /scans API (' + result.count + ' scans)', 'PASS', Date.now() - t0);
    } catch (e) {
      utils.record(SUITE, 'TC-055 /scans API returns array', 'FAIL', Date.now() - t0, e.message);
      throw e;
    }
  });

  it('TC-056 · All sidebar nav links are accessible', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/dashboard');
      await driver.sleep(800);
      const links = await driver.findElements(By.css('.sidebar nav a'));
      expect(links.length).to.be.at.least(4);
      const hrefs = await Promise.all(links.map(l => l.getAttribute('href')));
      const valid = hrefs.filter(h => h && h.startsWith('http'));
      expect(valid.length).to.be.at.least(4);
      utils.record(SUITE, 'TC-056 Sidebar nav links = ' + valid.length, 'PASS', Date.now() - t0);
    } catch (e) {
      utils.record(SUITE, 'TC-056 Sidebar nav links accessible', 'FAIL', Date.now() - t0, e.message);
      throw e;
    }
  });

  it('TC-057 · CSS stylesheet loads (body has dark background)', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/dashboard');
      await driver.sleep(600);
      const bgColor = await driver.executeScript(
        "return window.getComputedStyle(document.body).backgroundColor"
      );
      expect(bgColor).to.not.equal('rgba(0, 0, 0, 0)');
      expect(bgColor).to.not.equal('');
      const ss = await utils.screenshot(driver, 'TC057_css_loaded');
      utils.record(SUITE, 'TC-057 CSS loaded (bg=' + bgColor + ')', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC057_FAIL');
      utils.record(SUITE, 'TC-057 CSS stylesheet loads', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-058 · Lucide icons are injected (SVG elements present)', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/dashboard');
      await driver.sleep(1000);
      const svgs = await driver.findElements(By.css('svg'));
      expect(svgs.length).to.be.at.least(3);
      utils.record(SUITE, 'TC-058 Lucide icons injected (' + svgs.length + ' SVGs)', 'PASS', Date.now() - t0);
    } catch (e) {
      utils.record(SUITE, 'TC-058 Lucide icons injected', 'FAIL', Date.now() - t0, e.message);
      throw e;
    }
  });

  it('TC-059 · Responsive layout at 768px (mobile sidebar toggles)', async () => {
    const t0 = Date.now();
    try {
      await driver.manage().window().setRect({ width: 768, height: 900 });
      await utils.goto(driver, cfg.BASE_URL + '/dashboard');
      await driver.sleep(800);
      const toggle = await utils.exists(driver, By.css('#menu-toggle, .menu-toggle'));
      expect(toggle).to.be.true;
      const ss = await utils.screenshot(driver, 'TC059_mobile_layout');
      await driver.manage().window().setRect({ width: 1400, height: 900 });
      utils.record(SUITE, 'TC-059 Mobile sidebar toggle visible at 768px', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      await driver.manage().window().setRect({ width: 1400, height: 900 }).catch(() => {});
      const ss = await utils.screenshot(driver, 'TC059_FAIL');
      utils.record(SUITE, 'TC-059 Responsive layout', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });

  it('TC-060 · Sign-out button logs out and redirects to login', async () => {
    const t0 = Date.now();
    try {
      await utils.goto(driver, cfg.BASE_URL + '/dashboard');
      await driver.sleep(800);
      const logoutBtn = await driver.findElement(By.css('.logout-btn'));
      await driver.executeScript('arguments[0].click()', logoutBtn);
      await driver.sleep(1500);
      const url = await driver.getCurrentUrl();
      expect(url).to.include('/login');
      const ss = await utils.screenshot(driver, 'TC060_logout');
      utils.record(SUITE, 'TC-060 Logout redirects to login', 'PASS', Date.now() - t0, '', ss);
    } catch (e) {
      const ss = await utils.screenshot(driver, 'TC060_FAIL');
      utils.record(SUITE, 'TC-060 Logout redirects to login', 'FAIL', Date.now() - t0, e.message, ss);
      throw e;
    }
  });
});
