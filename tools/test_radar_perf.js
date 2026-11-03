const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  const start = Date.now();
  await page.goto('http://localhost:8080/interactive_pages/parole-spia.html');
  const navTime = Date.now() - start;

  const headerPresent = await page.evaluate(() => !!document.getElementById('globalPortalNav'));
  const dockPresent = await page.evaluate(() => !!document.getElementById('nativeBottomDock'));

  console.log('Navigation Time:', navTime, 'ms');
  console.log('Header Present:', headerPresent);
  console.log('Dock Present:', dockPresent);
  console.log('Console Errors:', JSON.stringify(consoleErrors));

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_radar_instant_header.png' });
  console.log('Saved screenshot successfully');

  await browser.close();
})();
