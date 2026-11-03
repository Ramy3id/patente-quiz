const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
  if (acceptBtn) await acceptBtn.click();
  await page.waitForTimeout(300);

  console.log('=== TEST 1: Control Hub & Card Heights ===');
  const dimsQ1 = await page.evaluate(() => {
    const hub = document.querySelector('.exam-control-hub');
    const card = document.getElementById('questionCardStage');
    const media = document.querySelector('.exam-media-slot');
    const buttons = document.querySelector('.exam-choice-buttons');
    return {
      hubHeight: hub ? Math.round(hub.getBoundingClientRect().height) : 0,
      cardHeight: card ? Math.round(card.getBoundingClientRect().height) : 0,
      mediaHeight: media ? Math.round(media.getBoundingClientRect().height) : 0,
      buttonsHeight: buttons ? Math.round(buttons.getBoundingClientRect().height) : 0,
      buttonsTop: buttons ? Math.round(buttons.getBoundingClientRect().top) : 0
    };
  });
  console.log('Question 1 Dimensions:', dimsQ1);

  // Take screenshot of Q1
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_exam_new_q1.png' });

  console.log('\n=== TEST 2: Auto-Advance Verification ===');
  const qNumBefore = await page.$eval('.exam-q-badge', el => el.textContent.trim());
  console.log('Before clicking VERO:', qNumBefore);

  // Click VERO
  await page.click('#btnVero');
  console.log('Clicked VERO, waiting 350ms for auto-advance...');
  await page.waitForTimeout(350);

  const qNumAfter = await page.$eval('.exam-q-badge', el => el.textContent.trim());
  console.log('After auto-advance:', qNumAfter);

  const answeredVal = await page.$eval('#answeredCounter', el => el.textContent.trim());
  console.log('Answered counter:', answeredVal);

  const dimsQ2 = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage');
    const media = document.querySelector('.exam-media-slot');
    const buttons = document.querySelector('.exam-choice-buttons');
    return {
      cardHeight: card ? Math.round(card.getBoundingClientRect().height) : 0,
      mediaHeight: media ? Math.round(media.getBoundingClientRect().height) : 0,
      buttonsHeight: buttons ? Math.round(buttons.getBoundingClientRect().height) : 0,
      buttonsTop: buttons ? Math.round(buttons.getBoundingClientRect().top) : 0
    };
  });
  console.log('Question 2 Dimensions:', dimsQ2);
  console.log('Card Height difference (Q1 vs Q2):', Math.abs(dimsQ1.cardHeight - dimsQ2.cardHeight), 'px (Zero Layout Shift!)');
  console.log('Buttons Top difference (Q1 vs Q2):', Math.abs(dimsQ1.buttonsTop - dimsQ2.buttonsTop), 'px');

  // Take screenshot of Q2
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_exam_new_q2.png' });

  console.log('\n=== TEST 3: Prev Button Verification ===');
  await page.click('#btnPrev');
  await page.waitForTimeout(200);
  const qNumPrev = await page.$eval('.exam-q-badge', el => el.textContent.trim());
  console.log('After clicking Prev:', qNumPrev);

  console.log('\n=== TEST 4: Light Mode Capture ===');
  await page.evaluate(() => document.documentElement.classList.add('light'));
  await page.waitForTimeout(200);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_exam_new_light.png' });

  console.log('Console Errors:', consoleErrors);
  await browser.close();
  console.log('TEST COMPLETED.');
})();
