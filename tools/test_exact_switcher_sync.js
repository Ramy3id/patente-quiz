const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  const btn = page.locator('button:has-text("قبول ومتابعة")');
  if (await btn.isVisible()) {
    await btn.click();
    await page.waitForTimeout(300);
  }

  // 1. Capture Modern Skin Switcher
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_switcher_in_modern.png' });

  // 2. Click Official (🖥️ رسمي) button inside modern switcher
  await page.locator('#btnSkinMoto').click();
  await page.waitForTimeout(200);

  // 3. Capture Official Skin Switcher in Light Mode
  await page.evaluate(() => {
    document.documentElement.classList.add('light');
    localStorage.setItem('patente_theme', 'light');
  });
  await page.waitForTimeout(100);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_switcher_in_official_light.png' });

  // 4. Capture Official Skin Switcher in Dark Mode
  await page.evaluate(() => {
    document.documentElement.classList.remove('light');
    localStorage.setItem('patente_theme', 'dark');
  });
  await page.waitForTimeout(100);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_switcher_in_official_dark.png' });

  // 5. Click Modern (🌟 عصري) inside Official Skin switcher
  await page.locator('#btnSkinModernMoto').click();
  await page.waitForTimeout(200);

  const returnedToModern = await page.evaluate(() => !document.body.classList.contains('skin-moto'));
  console.log('Returned to Modern via sync button:', returnedToModern);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_returned_to_modern_via_sync.png' });

  await browser.close();
  console.log('Switcher sync test finished successfully.');
})();
