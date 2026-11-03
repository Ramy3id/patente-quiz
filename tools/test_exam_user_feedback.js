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

  // 1. Screenshot of Modern Question 1 (Check active pill highlight & separator line)
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_pill_active_highlight.png' });

  // 2. Click Flag Review button
  await page.locator('#btnModernFlag').click();
  await page.waitForTimeout(100);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_flag_above_separator.png' });

  // 3. Click Toggle Translation (Check translation open without scroll)
  await page.locator('#btnToggleTr').click();
  await page.waitForTimeout(100);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_tr_opened_no_scroll.png' });

  // 4. Switch to Official Skin (in Light Mode)
  await page.locator('#btnSkinMoto').click();
  await page.waitForTimeout(200);

  // Ensure Light Mode is active on HTML
  await page.evaluate(() => {
    document.documentElement.classList.add('light');
    localStorage.setItem('patente_theme', 'light');
  });
  await page.waitForTimeout(100);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_official_skin_light_mode.png' });

  // 5. Official Skin in Dark Mode
  await page.evaluate(() => {
    document.documentElement.classList.remove('light');
    localStorage.setItem('patente_theme', 'dark');
  });
  await page.waitForTimeout(100);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_official_skin_dark_mode.png' });

  await browser.close();
  console.log('User feedback testing screenshots generated successfully.');
})();
