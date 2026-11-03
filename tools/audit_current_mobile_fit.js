const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 667 } }); // Small phone!
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page.waitForTimeout(800);

  // Set Question 7 (Longest question)
  await page.evaluate(() => {
    exam.questions = [
      {
        id: 102,
        domanda: 'Fuori dei centri abitati, i conducenti devono spegnere i proiettori di profondità procedendo con quelli anabbaglianti, quando seguono un veicolo a breve distanza',
        risposta: true,
        img: 'immagini/276.png',
        immagine: 'immagini/276.png',
        traduzione: 'خارج المناطق السكنية، يجب على السائقين إطفاء المصابيح العالية وتشغيل المصابيح المنخفضة عندما يتبعون مركبة على مسافة قريبة.'
      }
    ];
    exam.currentIndex = 0;
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(300);

  // Test button position before opening translation
  const btnPosBefore = await page.evaluate(() => {
    const btn = document.getElementById('btnToggleTr');
    const r = btn.getBoundingClientRect();
    return { top: Math.round(r.top), left: Math.round(r.left) };
  });

  // Open translation
  await page.locator('#btnToggleTr').click();
  await page.waitForTimeout(300);

  // Measure button position after opening translation
  const btnPosAfter = await page.evaluate(() => {
    const btn = document.getElementById('btnToggleTr');
    const r = btn.getBoundingClientRect();
    return { top: Math.round(r.top), left: Math.round(r.left) };
  });

  console.log('Toggle Button Position - Before:', btnPosBefore, '| After:', btnPosAfter);

  const screenMetrics = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage').getBoundingClientRect();
    const submitBtn = document.getElementById('btnModernSubmit').getBoundingClientRect();
    const nextBtn = document.getElementById('btnNext').getBoundingClientRect();
    const prevBtn = document.getElementById('btnPrev').getBoundingClientRect();
    const flagBtn = document.getElementById('btnModernFlag').getBoundingClientRect();
    const badge = document.querySelector('.exam-q-badge').getBoundingClientRect();
    const tc = document.querySelector('.exam-text-container');
    const tr = document.getElementById('examArabicText').getBoundingClientRect();

    return {
      viewportHeight: window.innerHeight,
      cardHeight: Math.round(card.height),
      cardBottom: Math.round(card.bottom),
      submitBtn: { top: Math.round(submitBtn.top), bottom: Math.round(submitBtn.bottom), isFullyVisible: submitBtn.bottom <= window.innerHeight },
      nextBtn: { isFullyVisible: nextBtn.bottom <= window.innerHeight },
      prevBtn: { isFullyVisible: prevBtn.bottom <= window.innerHeight },
      flagBtnHeight: Math.round(flagBtn.height),
      badgeHeight: Math.round(badge.height),
      textScrollHeight: tc.scrollHeight,
      textClientHeight: tc.clientHeight,
      hasScrollbar: tc.scrollHeight > tc.clientHeight
    };
  });
  console.log('Metrics on 375x667 screen:', screenMetrics);

  await browser.close();
})();
