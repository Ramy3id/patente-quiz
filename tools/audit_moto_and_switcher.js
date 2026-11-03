const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page.waitForTimeout(800);

  // Switch to Moto
  await page.locator('#btnSkinMoto').click();
  await page.waitForTimeout(400);

  // Set the 2 questions: Q1 Barrier, Q2 Long Question
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

  // Measure all sections of moto
  const motoMetrics = await page.evaluate(() => {
    const wrap = document.getElementById('motoScreenWrap').getBoundingClientRect();
    const header = document.querySelector('.moto-top-header').getBoundingClientRect();
    const signBox = document.getElementById('motoSignBox').getBoundingClientRect();
    const signImg = document.getElementById('motoSignImg').getBoundingClientRect();
    const qPanel = document.querySelector('.moto-question-panel').getBoundingClientRect();
    const qText = document.getElementById('motoQuestionText').getBoundingClientRect();
    const veroBtn = document.getElementById('btnMotoVero').getBoundingClientRect();
    const bottomControls = document.querySelector('.moto-bottom-controls').getBoundingClientRect();
    const matrix = document.getElementById('motoMatrixGrid').getBoundingClientRect();
    const concludeBtn = document.getElementById('btnMotoConclude').getBoundingClientRect();
    const switcher = document.getElementById('motoSkinSwitcher').getBoundingClientRect();

    return {
      viewportHeight: window.innerHeight,
      wrap: { top: wrap.top, bottom: wrap.bottom, height: wrap.height },
      header: { top: header.top, bottom: header.bottom, height: header.height },
      switcher: { top: switcher.top, left: switcher.left, width: switcher.width, height: switcher.height },
      signBox: { height: signBox.height },
      signImg: { width: signImg.width, height: signImg.height },
      qText: { height: qText.height, scrollHeight: document.getElementById('motoQuestionText').scrollHeight },
      veroBtn: { height: veroBtn.height, top: veroBtn.top },
      matrix: { height: matrix.height },
      concludeBtn: { top: concludeBtn.top, bottom: concludeBtn.bottom, height: concludeBtn.height },
      totalBottomOverflow: wrap.bottom - window.innerHeight
    };
  });
  console.log('Moto Screen Metrics:', JSON.stringify(motoMetrics, null, 2));

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/moto_deep_audit.png' });

  // Now measure Modern switcher position to compare!
  await page.locator('#btnSkinModernMoto').click();
  await page.waitForTimeout(400);

  const modernMetrics = await page.evaluate(() => {
    const switcher = document.querySelector('.exam-control-hub .exam-skin-switcher-mini').getBoundingClientRect();
    return {
      modernSwitcher: { top: switcher.top, left: switcher.left, width: switcher.width, height: switcher.height }
    };
  });
  console.log('Modern Switcher Metrics:', JSON.stringify(modernMetrics, null, 2));

  await browser.close();
})();
