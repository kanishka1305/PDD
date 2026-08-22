'use strict';
const { Builder, Browser } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const path   = require('path');

const CHROME_BIN = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

function buildDriver(headless = true) {
  const opts = new chrome.Options();
  opts.setChromeBinaryPath(CHROME_BIN);
  if (headless) {
    opts.addArguments('--headless=new');
  }
  opts.addArguments(
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--window-size=1400,900',
    '--disable-extensions',
    '--disable-popup-blocking',
    '--ignore-certificate-errors'
  );
  return new Builder()
    .forBrowser(Browser.CHROME)
    .setChromeOptions(opts)
    .build();
}

module.exports = { buildDriver };
