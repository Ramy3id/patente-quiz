const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  
  // 1. Check index.html (Home Page Chapter Cards) in both Dark & Light
  for (const mode of ['dark', 'light']) {
    const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
    await page.goto('http://localhost:8080/Capitoli_Divisi/index.html');
    
    // Dismiss GDPR
    const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
    if (acceptBtn) await acceptBtn.click();
    await page.waitForTimeout(200);

    if (mode === 'light') {
      await page.evaluate(() => document.documentElement.classList.add('light'));
    } else {
      await page.evaluate(() => document.documentElement.classList.remove('light'));
    }
    await page.waitForTimeout(200);

    const titleColor = await page.evaluate(() => {
      const el = document.querySelector('.ch-title-ar');
      return el ? window.getComputedStyle(el).color : null;
    });

    console.log(`[index.html - ${mode}] .ch-title-ar color:`, titleColor);

    // Scroll to chapter 1 card and take screenshot
    const cardEl = await page.$('.chapter-card');
    if (cardEl) {
      await cardEl.scrollIntoViewIfNeeded();
      await page.waitForTimeout(200);
      await cardEl.screenshot({
        path: `C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_card_${mode}.png`
      });
      console.log(`Saved screenshot verified_card_${mode}.png`);
    }

    await page.close();
  }

  // 2. Check scheda-esame.html (Exam Simulator Quiz Card) in both Dark & Light
  for (const mode of ['dark', 'light']) {
    const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
    await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');

    // Dismiss GDPR if any
    const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
    if (acceptBtn) await acceptBtn.click();
    await page.waitForTimeout(200);

    if (mode === 'light') {
      await page.evaluate(() => document.documentElement.classList.add('light'));
    } else {
      await page.evaluate(() => document.documentElement.classList.remove('light'));
    }
    await page.waitForTimeout(200);

    const veroStyle = await page.evaluate(() => {
      const el = document.querySelector('.choice-btn-vero');
      if (!el) return null;
      const cs = window.getComputedStyle(el);
      return { color: cs.color, bg: cs.backgroundColor, border: cs.borderColor };
    });
    const falsoStyle = await page.evaluate(() => {
      const el = document.querySelector('.choice-btn-falso');
      if (!el) return null;
      const cs = window.getComputedStyle(el);
      return { color: cs.color, bg: cs.backgroundColor, border: cs.borderColor };
    });

    console.log(`[scheda-esame - ${mode}] VERO:`, veroStyle);
    console.log(`[scheda-esame - ${mode}] FALSO:`, falsoStyle);

    // Click VERO to see answer feedback and explanation
    const btnVero = await page.$('#btnVero');
    if (btnVero) {
      await btnVero.click();
      await page.waitForTimeout(300);
    }

    const qCard = await page.$('.exam-card') || await page.$('.q-card') || await page.$('.exam-content-area');
    if (qCard) {
      await qCard.screenshot({
        path: `C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_quiz_${mode}.png`
      });
      console.log(`Saved screenshot verified_quiz_${mode}.png`);
    }

    await page.close();
  }

  await browser.close();
  console.log('ALL VERIFICATIONS FINISHED.');
})();
