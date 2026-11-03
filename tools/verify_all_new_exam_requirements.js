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

  // 1. Verify Modern Skin Default (Arabic Translation Hidden)
  const trDefaultVisible = await page.locator('#examArabicText').isVisible();
  console.log('1. Modern - Arabic translation default visible:', trDefaultVisible); // Should be false
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_modern_tr_closed.png' });

  // 2. Click Flag Review button
  await page.locator('#btnModernFlag').click();
  await page.waitForTimeout(100);
  const flagText = await page.locator('#btnModernFlag').textContent();
  console.log('2. Modern - Flag button text after click:', flagText.trim());
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_modern_flag_active.png' });

  // 3. Click Toggle Translation Button
  await page.locator('#btnToggleTr').click();
  await page.waitForTimeout(100);
  const trOpenedVisible = await page.locator('#examArabicText').isVisible();
  console.log('3. Modern - Arabic translation opened visible:', trOpenedVisible); // Should be true
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_modern_tr_opened.png' });

  // 4. Switch to Official Motorizzazione Skin
  await page.locator('#btnSkinMoto').click();
  await page.waitForTimeout(200);

  // Check Official Skin properties
  const isMotoActive = await page.evaluate(() => document.body.classList.contains('skin-moto'));
  const isReturnBtnVisible = await page.locator('#btnMotoReturnModern').isVisible();
  const isHelperPresent = await page.locator('.moto-arabic-helper').isVisible();
  console.log('4. Official Skin active:', isMotoActive);
  console.log('5. Return to modern button visible:', isReturnBtnVisible);
  console.log('6. Arabic helper visible in Official:', isHelperPresent); // Should be false

  // Official dimensions test
  const motoDims = await page.evaluate(() => {
    const wrap = document.getElementById('motoScreenWrap');
    const signBox = document.getElementById('motoSignBox');
    const touchButtons = document.querySelector('.moto-touch-buttons-grid');
    return {
      wrapHeight: Math.round(wrap.getBoundingClientRect().height),
      signHeight: Math.round(signBox.getBoundingClientRect().height),
      touchButtonsTop: Math.round(touchButtons.getBoundingClientRect().top)
    };
  });
  console.log('7. Official Screen Dims:', motoDims);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_official_skin_q1.png' });

  // 8. Test Auto-advance in Official Skin
  const initialMotoBadge = await page.locator('#motoQuestionBadge').textContent();
  console.log('8. Initial Official Question:', initialMotoBadge.trim());
  await page.locator('#btnMotoVero').click();
  await page.waitForTimeout(350); // wait for 220ms auto-advance
  const nextMotoBadge = await page.locator('#motoQuestionBadge').textContent();
  console.log('9. Official after auto-advance Question:', nextMotoBadge.trim());
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_official_skin_auto_advanced.png' });

  // 10. Test Return to Modern Skin
  await page.locator('#btnMotoReturnModern').click();
  await page.waitForTimeout(200);
  const returnedToModern = await page.evaluate(() => !document.body.classList.contains('skin-moto'));
  console.log('10. Successfully returned to Modern Skin:', returnedToModern);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_returned_to_modern.png' });

  await browser.close();
  console.log('ALL VERIFICATION STEPS COMPLETED.');
})();
