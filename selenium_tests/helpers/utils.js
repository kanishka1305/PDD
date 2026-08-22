'use strict';
const { By, until } = require('selenium-webdriver');
const fs   = require('fs');
const path = require('path');
const cfg  = require('./config');

/* ── Wait for element ─────────────────────────────────────────── */
async function waitFor(driver, locator, timeout = cfg.TIMEOUT) {
  return driver.wait(until.elementLocated(locator), timeout);
}

async function waitVisible(driver, locator, timeout = cfg.TIMEOUT) {
  const el = await driver.wait(until.elementLocated(locator), timeout);
  await driver.wait(until.elementIsVisible(el), timeout);
  return el;
}

async function waitClickable(driver, locator, timeout = cfg.TIMEOUT) {
  const el = await driver.wait(until.elementLocated(locator), timeout);
  await driver.wait(until.elementIsEnabled(el), timeout);
  return el;
}

/* ── Safe click (scroll into view first) ─────────────────────── */
async function click(driver, locator) {
  const el = await waitClickable(driver, locator);
  await driver.executeScript('arguments[0].scrollIntoView({block:"center"});', el);
  await driver.sleep(150);
  await el.click();
  return el;
}

/* ── Type into input ─────────────────────────────────────────── */
async function type(driver, locator, text) {
  const el = await waitVisible(driver, locator);
  await el.clear();
  await el.sendKeys(text);
}

/* ── Get text safely ──────────────────────────────────────────── */
async function getText(driver, locator) {
  try {
    const el = await waitVisible(driver, locator, 5000);
    return (await el.getText()).trim();
  } catch { return ''; }
}

/* ── Check element exists ─────────────────────────────────────── */
async function exists(driver, locator, timeout = 4000) {
  try {
    await driver.wait(until.elementLocated(locator), timeout);
    return true;
  } catch { return false; }
}

/* ── Screenshot ───────────────────────────────────────────────── */
async function screenshot(driver, name) {
  try {
    if (!fs.existsSync(cfg.SCREENSHOT_DIR)) fs.mkdirSync(cfg.SCREENSHOT_DIR, { recursive: true });
    const data = await driver.takeScreenshot();
    const file = path.join(cfg.SCREENSHOT_DIR, `${name}_${Date.now()}.png`);
    fs.writeFileSync(file, data, 'base64');
    return file;
  } catch { return null; }
}

/* ── Navigate and wait for page ready ────────────────────────── */
async function goto(driver, url) {
  await driver.get(url);
  await driver.sleep(cfg.SHORT_WAIT);
}

/* ── Global test results collector ───────────────────────────── */
const results = [];

function record(suite, name, status, duration, error = '', screenshotPath = '') {
  results.push({
    suite, name, status, duration,
    error: error ? String(error).substring(0, 300) : '',
    screenshot: screenshotPath,
    timestamp: new Date().toISOString(),
  });
}

function getResults() { return results; }

function saveResults() {
  if (!fs.existsSync(cfg.REPORT_DIR)) fs.mkdirSync(cfg.REPORT_DIR, { recursive: true });
  const file = path.join(cfg.REPORT_DIR, 'test_results.json');
  fs.writeFileSync(file, JSON.stringify(results, null, 2));
  return file;
}

module.exports = {
  waitFor, waitVisible, waitClickable,
  click, type, getText, exists,
  screenshot, goto,
  record, getResults, saveResults,
};
