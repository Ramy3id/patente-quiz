const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });

  const consoleLogs = [];
  page.on('console', msg => consoleLogs.push({ type: msg.type(), text: msg.text() }));
  page.on('pageerror', err => consoleLogs.push({ type: 'pageerror', text: err.message }));

  const failedRequests = [];
  page.on('requestfailed', req => failedRequests.push({ url: req.url(), failure: req.failure() }));

  const response = await page.goto('http://localhost:8080/interactive_pages/parole-spia.html');
  await page.waitForTimeout(2000);

  console.log('Status code:', response.status());
  console.log('Console logs:', consoleLogs);
  console.log('Failed requests:', failedRequests);

  const pageData = await page.evaluate(() => {
    return {
      title: document.title,
      totalCountText: document.getElementById('countAll')?.textContent,
      wordsData: window.PAROLE_SPIA_DATA ? window.PAROLE_SPIA_DATA.length : 'undefined',
      questionsData: window.ALL_QUESTIONS_DATA ? window.ALL_QUESTIONS_DATA.length : 'undefined',
      gridInnerHTML: document.getElementById('wordsGrid')?.innerHTML?.substring(0, 300)
    };
  });
  console.log('Page Data in Browser:', pageData);

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/parole_spia_debug.png' });

  await browser.close();
})();
