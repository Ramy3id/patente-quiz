const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  const acceptBtn = await page.locator('button:has-text("قبول ومتابعة")').first();
  if (await acceptBtn.isVisible()) {
    await acceptBtn.click();
  }
  await page.waitForTimeout(300);

  // Question 0
  await page.evaluate(() => {
    exam.goToQuestion(0);
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(100);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_exam_q0.png' });

  // Question 1 (Long text with image)
  await page.evaluate(() => {
    exam.goToQuestion(1);
    renderActiveQuestion();
    renderPills();
  });
  await page.waitForTimeout(100);
  const dimsQ1 = await page.evaluate(() => {
    const card = document.getElementById('questionCardStage');
    const media = document.querySelector('.exam-media-slot');
    const buttons = document.querySelector('.exam-choice-buttons');
    return {
      cardHeight: Math.round(card.getBoundingClientRect().height),
      mediaHeight: Math.round(media.getBoundingClientRect().height),
      buttonsTop: Math.round(buttons.getBoundingClientRect().top)
    };
  });
  console.log('Q1 (Long text with image) Dims:', dimsQ1);
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_exam_long_q1.png' });

  // Find a question without image
  const noImgIdx = await page.evaluate(() => {
    return exam.questions.findIndex(q => !q.img && !q.immagine);
  });
  if (noImgIdx !== -1) {
    await page.evaluate((idx) => {
      exam.goToQuestion(idx);
      renderActiveQuestion();
      renderPills();
    }, noImgIdx);
    await page.waitForTimeout(100);
    const dimsNoImg = await page.evaluate(() => {
      const card = document.getElementById('questionCardStage');
      const media = document.querySelector('.exam-media-slot');
      const buttons = document.querySelector('.exam-choice-buttons');
      return {
        cardHeight: Math.round(card.getBoundingClientRect().height),
        mediaHeight: Math.round(media.getBoundingClientRect().height),
        buttonsTop: Math.round(buttons.getBoundingClientRect().top)
      };
    });
    console.log('No-Img Question Dims:', dimsNoImg);
    await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_exam_no_img.png' });
  }

  await browser.close();
  console.log('All screenshots captured successfully.');
})();
