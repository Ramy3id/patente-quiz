const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/Capitoli_Divisi/index.html');
  const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
  if (acceptBtn) await acceptBtn.click();
  await page.waitForTimeout(300);

  await page.evaluate(() => window.scrollTo(0, 1500));
  await page.waitForTimeout(500);

  await page.screenshot({
    path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_scroll_btn_visible.png',
    clip: { x: 10, y: 660, width: 80, height: 80 }
  });
  console.log('Saved scroll btn visible screenshot');

  await browser.close();
})();
