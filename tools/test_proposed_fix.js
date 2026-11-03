const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page.waitForTimeout(1000);

  // Apply proposed CSS overrides live in page to inspect before writing to file
  await page.addStyleTag({
    content: `
      .exam-question-card {
        padding: 16px 14px 34px !important;
        border-radius: 24px !important;
      }
      .exam-media-slot {
        height: 150px !important;
        min-height: 150px !important;
        max-height: 150px !important;
        margin: 4px 0 8px !important;
      }
      .exam-sign-frame img {
        max-height: 140px !important;
        max-width: 260px !important;
        object-fit: contain !important;
      }
      .exam-text-container {
        height: 280px !important;
        min-height: 280px !important;
        max-height: 280px !important;
        overflow-y: hidden !important;
        margin: 4px 0 8px !important;
        padding: 4px 8px !important;
      }
      .exam-text-it {
        font-size: 1.02rem !important;
        line-height: 1.38 !important;
        margin: 0 0 6px !important;
      }
      .exam-tr-wrapper {
        margin-top: auto !important;
        margin-bottom: 2px !important;
        gap: 6px !important;
      }
      .exam-text-tr {
        font-size: 0.88rem !important;
        line-height: 1.38 !important;
        padding: 8px 12px !important;
      }
      .exam-choice-buttons {
        gap: 10px !important;
        margin: 6px 0 !important;
      }
      .choice-btn {
        height: 52px !important;
        min-height: 52px !important;
        max-height: 52px !important;
      }
      .exam-nav-steps {
        display: grid !important;
        grid-template-columns: 1fr auto 1fr !important;
        align-items: center !important;
        gap: 8px !important;
        margin-top: 14px !important;
        margin-bottom: 4px !important;
        height: 44px !important;
        min-height: 44px !important;
        border-top: none !important;
        padding: 0 2px !important;
      }
      .btn-nav-step {
        height: 44px !important;
        min-height: 44px !important;
        padding: 0 14px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
      }
      .btn-submit-pill {
        height: 44px !important;
        min-height: 44px !important;
        padding: 0 14px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 12px !important;
      }
    `
  });

  // Test Q1: Barrier
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

  const q1Dims = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const navSteps = document.querySelector('.exam-nav-steps').getBoundingClientRect();
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    const img = document.querySelector('.exam-media-slot img').getBoundingClientRect();
    return {
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      submitBtnBottom: Math.round(submitBtn.bottom),
      paddingBelowButtons: Math.round(card.bottom - submitBtn.bottom),
      imgRendered: { width: Math.round(img.width), height: Math.round(img.height) }
    };
  });
  console.log('Q1 (Barrier) Dims:', q1Dims);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_new_q1_barrier.png' });

  // Test Q2: Long Question with Translation
  await page.evaluate(() => {
    exam.currentIndex = 1;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(200);
  await page.locator('#btnToggleTr').click();
  await page.waitForTimeout(300);

  const q2Dims = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const textContainer = document.querySelector('.exam-text-container');
    const textRect = textContainer.getBoundingClientRect();
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    const trEl = document.getElementById('examArabicText');
    const trRect = trEl.getBoundingClientRect();
    return {
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      submitBtnBottom: Math.round(submitBtn.bottom),
      paddingBelowButtons: Math.round(card.bottom - submitBtn.bottom),
      textScrollHeight: textContainer.scrollHeight,
      textClientHeight: textContainer.clientHeight,
      hasScrollbar: textContainer.scrollHeight > textContainer.clientHeight,
      trVisible: trEl.offsetParent !== null,
      trBottom: Math.round(trRect.bottom),
      textContainerBottom: Math.round(textRect.bottom),
      trInsideContainer: Math.round(textRect.bottom - trRect.bottom)
    };
  });
  console.log('Q2 (Long Question) Dims:', q2Dims);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_new_q2_long_question.png' });

  await browser.close();
})();
