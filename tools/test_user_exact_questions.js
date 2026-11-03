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

  // 1. Find the question with the barrier or any image
  // Let's find question with barrier or sign
  const barrierIdx = await page.evaluate(() => {
    return exam.questions.findIndex(q => q.domanda.includes('barriera') || (q.img && q.img.includes('barriera')));
  });
  console.log('Barrier question index:', barrierIdx);
  const targetImgIdx = barrierIdx !== -1 ? barrierIdx : 4; // fallback to Q5

  await page.evaluate((idx) => {
    exam.goToQuestion(idx);
    renderActiveQuestion();
    renderPills();
  }, targetImgIdx);
  await page.waitForTimeout(200);

  // Measure card and buttons
  const cardDimsQ5 = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage');
    const navSteps = document.querySelector('.exam-nav-steps');
    const mediaSlot = document.querySelector('.exam-media-slot');
    const img = document.querySelector('.exam-sign-frame img');
    return {
      cardHeight: Math.round(card.getBoundingClientRect().height),
      cardBottom: Math.round(card.getBoundingClientRect().bottom),
      navStepsBottom: Math.round(navSteps.getBoundingClientRect().bottom),
      paddingInsideCard: Math.round(card.getBoundingClientRect().bottom - navSteps.getBoundingClientRect().bottom),
      mediaHeight: Math.round(mediaSlot.getBoundingClientRect().height),
      imgHeight: img ? Math.round(img.getBoundingClientRect().height) : null
    };
  });
  console.log('Q5 (Barrier image) Dims:', cardDimsQ5);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_q5_barrier_full.png' });

  // 2. Find the long question "Fuori dei centri abitati"
  const longQIdx = await page.evaluate(() => {
    return exam.questions.findIndex(q => q.domanda.includes('Fuori dei centri abitati') || q.domanda.includes('spegnere i proiettori'));
  });
  console.log('Long question index:', longQIdx);
  const targetLongIdx = longQIdx !== -1 ? longQIdx : 6; // fallback to Q7

  await page.evaluate((idx) => {
    exam.goToQuestion(idx);
    renderActiveQuestion();
    renderPills();
  }, targetLongIdx);
  await page.waitForTimeout(200);

  // Click toggle translation
  await page.locator('#btnToggleTr').click();
  await page.waitForTimeout(200);

  const cardDimsQ7 = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage');
    const navSteps = document.querySelector('.exam-nav-steps');
    const textContainer = document.querySelector('.exam-text-container');
    const arabicText = document.getElementById('examArabicText');
    return {
      cardHeight: Math.round(card.getBoundingClientRect().height),
      cardBottom: Math.round(card.getBoundingClientRect().bottom),
      navStepsBottom: Math.round(navSteps.getBoundingClientRect().bottom),
      paddingInsideCard: Math.round(card.getBoundingClientRect().bottom - navSteps.getBoundingClientRect().bottom),
      scrollHeight: textContainer.scrollHeight,
      clientHeight: textContainer.clientHeight,
      hasScrollbar: textContainer.scrollHeight > textContainer.clientHeight,
      arabicVisible: arabicText ? arabicText.offsetParent !== null : false
    };
  });
  console.log('Q7 (Long question with translation) Dims:', cardDimsQ7);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_q7_long_translation_no_scroll.png' });

  await browser.close();
  console.log('User exact questions verification finished.');
})();
