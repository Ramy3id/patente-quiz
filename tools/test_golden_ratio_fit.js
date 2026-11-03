const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();

  // Test 1: Standard Phone (375 x 812)
  console.log('--- TEST 1: Standard Mobile Viewport (375 x 812) ---');
  const page1 = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page1.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page1.waitForTimeout(800);

  // Set the 2 questions
  await page1.evaluate(() => {
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
  await page1.waitForTimeout(300);

  const q1Metrics812 = await page1.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    const img = document.querySelector('.exam-media-slot img');
    return {
      viewportHeight: window.innerHeight,
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      submitBtnBottom: Math.round(submitBtn.bottom),
      paddingBelowButtons: Math.round(card.bottom - submitBtn.bottom),
      fitsInsideScreen: card.bottom <= window.innerHeight,
      imgRendered: img ? { width: Math.round(img.getBoundingClientRect().width), height: Math.round(img.getBoundingClientRect().height) } : null
    };
  });
  console.log('375x812 Q1 (Barrier):', q1Metrics812);
  await page1.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_golden_q1_812.png' });

  // Q2 with translation
  await page1.evaluate(() => {
    exam.currentIndex = 1;
    renderActiveQuestion();
    renderPills();
  });
  await page1.waitForTimeout(200);
  await page1.locator('#btnToggleTr').click();
  await page1.waitForTimeout(300);

  const q2Metrics812 = await page1.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const tc = document.querySelector('.exam-text-container');
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    return {
      viewportHeight: window.innerHeight,
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      submitBtnBottom: Math.round(submitBtn.bottom),
      paddingBelowButtons: Math.round(card.bottom - submitBtn.bottom),
      fitsInsideScreen: card.bottom <= window.innerHeight,
      textScrollHeight: tc.scrollHeight,
      textClientHeight: tc.clientHeight,
      hasScrollbar: tc.scrollHeight > tc.clientHeight
    };
  });
  console.log('375x812 Q2 (Long + Translation):', q2Metrics812);
  await page1.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_golden_q2_812.png' });

  // Test 2: Compact Phone (375 x 667 - iPhone SE)
  console.log('--- TEST 2: Compact Mobile Viewport (375 x 667) ---');
  const page2 = await browser.newPage({ viewport: { width: 375, height: 667 } });
  await page2.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page2.waitForTimeout(800);

  await page2.evaluate(() => {
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
  await page2.waitForTimeout(300);

  const q1Metrics667 = await page2.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    return {
      viewportHeight: window.innerHeight,
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      fitsInsideScreen: card.bottom <= window.innerHeight
    };
  });
  console.log('375x667 Q1 (Barrier):', q1Metrics667);
  await page2.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_golden_q1_667.png' });

  await browser.close();
  console.log('GOLDEN RATIO TEST COMPLETED!');
})();
