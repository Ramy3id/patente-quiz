const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page.waitForTimeout(600);

  // Set Light Mode
  await page.evaluate(() => {
    document.documentElement.classList.add('light');
    document.documentElement.classList.remove('dark');
  });
  await page.waitForTimeout(200);

  // Switch to Official Skin
  await page.locator('#btnSkinMoto').click();
  await page.waitForTimeout(300);

  // Set Question 1 (Barrier)
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

  // Inspect computed style of text in light mode
  const textStyles = await page.evaluate(() => {
    const el = document.getElementById('motoQuestionText');
    const comp = window.getComputedStyle(el);
    const terminal = document.querySelector('.moto-main-terminal');
    const termComp = window.getComputedStyle(terminal);
    return {
      textColor: comp.color,
      fontSize: comp.fontSize,
      fontWeight: comp.fontWeight,
      terminalBg: termComp.backgroundColor
    };
  });
  console.log('Official Light Mode Text Computed Styles:', textStyles);

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_moto_light_q1_fixed.png' });

  // Now inspect Q2 (Long Question)
  await page.evaluate(() => {
    exam.currentIndex = 1;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(300);

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_moto_light_q2_fixed.png' });

  await browser.close();
  console.log('Official Light Mode text inspection completed!');
})();
