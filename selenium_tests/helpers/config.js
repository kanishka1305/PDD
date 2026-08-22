'use strict';

module.exports = {
  BASE_URL:      'http://localhost:8000',
  TEST_EMAIL:    'selenium@dentai.com',
  TEST_PASSWORD: 'Selenium@123',
  TEST_NAME:     'Selenium Doctor',
  TEST_LICENSE:  'SEL-000001',
  TIMEOUT:       20000,   // ms – element wait timeout
  PAGE_TIMEOUT:  15000,   // ms – page load timeout
  SHORT_WAIT:    500,
  MEDIUM_WAIT:   1500,
  SCREENSHOT_DIR: require('path').join(__dirname, '..', 'screenshots'),
  REPORT_DIR:     require('path').join(__dirname, '..', 'reports'),
};
