const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  for (const mode of ['dark', 'light']) {
    const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
    await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
    const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
    if (acceptBtn) await acceptBtn.click();
    await page.waitForTimeout(200);

    if (mode === 'light') {
      await page.evaluate(() => document.documentElement.classList.add('light'));
    } else {
      await page.evaluate(() => document.documentElement.classList.remove('light'));
    }
    await page.waitForTimeout(200);

    const card = await page.$('#questionCardStage');
    if (card) {
      await card.screenshot({
        path: `C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_quiz_card_${mode}.png`
      });
      console.log(`Saved verified_quiz_card_${mode}.png`);
    }
    await page.close();
  }
  await browser.close();
})();
