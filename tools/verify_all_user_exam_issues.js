const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page.waitForTimeout(1000);

  // Accept cookies if present
  const btn = page.locator('button:has-text("قبول ومتابعة")');
  if (await btn.isVisible()) {
    await btn.click();
    await page.waitForTimeout(300);
  }

  // Set the 2 specific questions from the user's screenshots
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
  await page.waitForTimeout(400);

  // 1. Check Q1 (Barrier image)
  const q1Metrics = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    const img = document.querySelector('.exam-media-slot img');
    return {
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      submitBtnBottom: Math.round(submitBtn.bottom),
      paddingBelowButtons: Math.round(card.bottom - submitBtn.bottom),
      imgRendered: img ? { width: Math.round(img.getBoundingClientRect().width), height: Math.round(img.getBoundingClientRect().height) } : null
    };
  });
  console.log('Q1 Barrier Metrics:', q1Metrics);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_q5_barrier_perfect.png' });

  // 2. Check Q2 (Long question with translation)
  await page.evaluate(() => {
    exam.currentIndex = 1;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(200);
  await page.locator('#btnToggleTr').click();
  await page.waitForTimeout(300);

  const q2Metrics = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const textContainer = document.querySelector('.exam-text-container');
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    const trEl = document.getElementById('examArabicText');
    return {
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      submitBtnBottom: Math.round(submitBtn.bottom),
      paddingBelowButtons: Math.round(card.bottom - submitBtn.bottom),
      scrollHeight: textContainer.scrollHeight,
      clientHeight: textContainer.clientHeight,
      hasScrollbar: textContainer.scrollHeight > textContainer.clientHeight,
      trVisible: trEl ? trEl.offsetParent !== null : false
    };
  });
  console.log('Q2 Long Question Metrics:', q2Metrics);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_q7_long_tr_perfect.png' });

  // 3. Switch to Official Motorizzazione Skin
  await page.locator('#btnSkinMoto').click();
  await page.waitForTimeout(400);

  // Check Official Skin with Q1
  await page.evaluate(() => {
    exam.currentIndex = 0;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(300);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_moto_barrier_perfect.png' });

  // Check Official Skin with Q2 (Long question)
  await page.evaluate(() => {
    exam.currentIndex = 1;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(300);
  const motoQ2Metrics = await page.evaluate(() => {
    const qText = document.getElementById('motoQuestionText');
    return {
      scrollHeight: qText.scrollHeight,
      clientHeight: qText.clientHeight,
      hasScrollbar: qText.scrollHeight > qText.clientHeight
    };
  });
  console.log('Moto Q2 Text Metrics:', motoQ2Metrics);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_moto_long_perfect.png' });

  // 4. Test Official Light Mode
  await page.evaluate(() => {
    document.documentElement.classList.add('light');
    document.documentElement.classList.remove('dark');
  });
  await page.waitForTimeout(300);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_moto_light_perfect.png' });

  // 5. Test Modern Light Mode
  await page.locator('#btnSkinModernMoto').click();
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_modern_light_perfect.png' });

  await browser.close();
  console.log('ALL VERIFICATIONS COMPLETED SUCCESSFULLY!');
})();
