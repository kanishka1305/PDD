'use strict';
const { By }  = require('selenium-webdriver');
const cfg     = require('./config');
const utils   = require('./utils');

/* ── Register test account (safe to call multiple times) ─────── */
async function ensureAccount(driver) {
  await utils.goto(driver, cfg.BASE_URL + '/signup');
  try {
    await utils.type(driver, By.id('name'),     cfg.TEST_NAME);
    await utils.type(driver, By.id('license'),  cfg.TEST_LICENSE);
    await utils.type(driver, By.id('email'),    cfg.TEST_EMAIL);
    await utils.type(driver, By.id('password'), cfg.TEST_PASSWORD);
    await utils.click(driver, By.css('button[type=submit]'));
    await driver.sleep(1000);
  } catch (_) { /* already exists — that's fine */ }
}

/* ── Login and store token in localStorage ───────────────────── */
async function login(driver) {
  await utils.goto(driver, cfg.BASE_URL + '/login');
  await utils.type(driver, By.id('email'),    cfg.TEST_EMAIL);
  await utils.type(driver, By.id('password'), cfg.TEST_PASSWORD);
  await utils.click(driver, By.css('button[type=submit]'));
  await driver.sleep(1500);

  // Inject user into localStorage if not set (in case backend session differs)
  await driver.executeScript(`
    if (!localStorage.getItem('user')) {
      localStorage.setItem('user', JSON.stringify({
        id: 1, name: '${cfg.TEST_NAME}', email: '${cfg.TEST_EMAIL}'
      }));
    }
  `);
}

/* ── Quick inject (skip login form for non-auth tests) ────────── */
async function injectAuth(driver) {
  await driver.executeScript(`
    localStorage.setItem('user', JSON.stringify({
      id: 1, name: '${cfg.TEST_NAME}', email: '${cfg.TEST_EMAIL}'
    }));
  `);
}

module.exports = { ensureAccount, login, injectAuth };
