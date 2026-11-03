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

  // Force questions to be the user's questions:
  await page.evaluate(() => {
    exam.questions = [
      {
        id: 101,
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

  // Take screenshot of Q1 (Barrier)
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/test_barrier_actual.png' });

  // Go to Q2 (Long question) and open translation
  await page.evaluate(() => {
    exam.currentIndex = 1;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(200);
  await page.locator('#btnToggleTr').click();
  await page.waitForTimeout(300);

  // Take screenshot of Q2 (Long question with translation)
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/test_long_actual.png' });

  // Get bounding rects for Q2
  const rects = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const textContainer = document.querySelector('.exam-text-container').getBoundingClientRect();
    const navSteps = document.querySelector('.exam-nav-steps').getBoundingClientRect();
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    const tc = document.querySelector('.exam-text-container');
    const imgEl = document.querySelector('.exam-media-slot img');
    return {
      card: { top: Math.round(card.top), bottom: Math.round(card.bottom), height: Math.round(card.height) },
      textContainer: { top: Math.round(textContainer.top), bottom: Math.round(textContainer.bottom), height: Math.round(textContainer.height), scrollHeight: tc.scrollHeight, clientHeight: tc.clientHeight },
      navSteps: { top: Math.round(navSteps.top), bottom: Math.round(navSteps.bottom), height: Math.round(navSteps.height) },
      submitBtn: { top: Math.round(submitBtn.top), bottom: Math.round(submitBtn.bottom), height: Math.round(submitBtn.height) },
      bottomGap: Math.round(card.bottom - submitBtn.bottom)
    };
  });
  console.log('Q2 rects:', JSON.stringify(rects, null, 2));

  await browser.close();
})();
