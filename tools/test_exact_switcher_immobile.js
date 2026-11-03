const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page.waitForTimeout(800);

  // Accept cookies if present
  const btn = page.locator('button:has-text("قبول ومتابعة")');
  if (await btn.isVisible()) {
    await btn.click();
    await page.waitForTimeout(300);
  }

  // 1. Measure switcher in Modern Mode
  const modernSwitcherRect = await page.evaluate(() => {
    const el = document.getElementById('masterSkinSwitcher');
    const r = el.getBoundingClientRect();
    return { top: Math.round(r.top * 100) / 100, left: Math.round(r.left * 100) / 100, width: Math.round(r.width * 100) / 100, height: Math.round(r.height * 100) / 100 };
  });
  console.log('Switcher in Modern:', modernSwitcherRect);

  // 2. Click Official (Moto) button
  await page.locator('#btnSkinMoto').click();
  await page.waitForTimeout(300);

  // 3. Measure switcher in Official Mode
  const motoSwitcherRect = await page.evaluate(() => {
    const el = document.getElementById('masterSkinSwitcher');
    const r = el.getBoundingClientRect();
    return { top: Math.round(r.top * 100) / 100, left: Math.round(r.left * 100) / 100, width: Math.round(r.width * 100) / 100, height: Math.round(r.height * 100) / 100 };
  });
  console.log('Switcher in Moto:', motoSwitcherRect);

  const deltaTop = Math.abs(modernSwitcherRect.top - motoSwitcherRect.top);
  const deltaLeft = Math.abs(modernSwitcherRect.left - motoSwitcherRect.left);
  console.log('DELTA TOP:', deltaTop, 'px | DELTA LEFT:', deltaLeft, 'px');

  // Verify questions in Official Mode
  await page.evaluate(() => {
    exam.questions = [
      {
        id: 39,
        domanda: 'La barriera raffigurata segnala una curva pericolosa',
        risposta: false,
        img: 'immagini/276.png',
        immagine: 'immagini/276.png',
        traduzione: 'تشير الحاجزة الموضحة إلى وجود منعطف خطر.'
      },
      {
        id: 102,
        domanda: 'Fuori dei centri abitati, i conducenti devono spegnere i proiettori di profondità procedendo con quelli anabbaglianti, quando seguono un veicolo a breve distanza',
        risposta: true,
        img: '',
        immagine: '',
        traduzione: 'خارج المناطق السكنية، يجب على السائقين إطفاء المصابيح العالية وتشغيل المصابيح المنخفضة عندما يتبعون مركبة على مسافة قريبة.'
      }
    ];
    exam.currentIndex = 0;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(300);

  // Official Q1 Barrier metrics
  const motoQ1Metrics = await page.evaluate(() => {
    const img = document.getElementById('motoSignImg');
    const box = document.getElementById('motoSignBox');
    const r = img.getBoundingClientRect();
    return {
      imgVisible: img.offsetParent !== null,
      imgWidth: Math.round(r.width),
      imgHeight: Math.round(r.height),
      boxHeight: Math.round(box.getBoundingClientRect().height)
    };
  });
  console.log('Official Q1 (Barrier) Metrics:', motoQ1Metrics);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_official_barrier_fixed.png' });

  // Test Auto-Advance on clicking VERO in Official Mode
  console.log('Testing Auto-Advance in Official Mode...');
  const idxBefore = await page.evaluate(() => exam.currentIndex);
  await page.locator('#btnMotoVero').click();
  await page.waitForTimeout(350); // wait for 220ms auto-advance
  const idxAfter = await page.evaluate(() => exam.currentIndex);
  console.log('Official Auto-Advance:', idxBefore, '->', idxAfter, '(Success:', idxAfter === 1, ')');

  // Official Q2 Long Question metrics
  const motoQ2Metrics = await page.evaluate(() => {
    const qText = document.getElementById('motoQuestionText');
    return {
      scrollHeight: qText.scrollHeight,
      clientHeight: qText.clientHeight,
      hasScrollbar: qText.scrollHeight > qText.clientHeight
    };
  });
  console.log('Official Q2 (Long Question) Metrics:', motoQ2Metrics);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_official_long_fixed.png' });

  // Test PRECEDENTE in Official Mode
  await page.locator('#btnMotoPrev').click();
  await page.waitForTimeout(200);
  const idxAfterPrev = await page.evaluate(() => exam.currentIndex);
  console.log('Official Precedente return:', idxAfterPrev, '(Success:', idxAfterPrev === 0, ')');

  // Test returning to Modern mode using the stationary button
  await page.locator('#btnSkinModern').click();
  await page.waitForTimeout(300);
  const returnModernRect = await page.evaluate(() => {
    const el = document.getElementById('masterSkinSwitcher');
    const r = el.getBoundingClientRect();
    return { top: Math.round(r.top * 100) / 100, left: Math.round(r.left * 100) / 100 };
  });
  console.log('Returned to Modern Switcher Rect:', returnModernRect);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_modern_returned_fixed.png' });

  await browser.close();
  console.log('TEST EXACT SWITCHER IMMOBILE COMPLETED!');
})();
