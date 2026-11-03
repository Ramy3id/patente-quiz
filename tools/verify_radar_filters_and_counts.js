const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/parole-spia.html');
  await page.waitForTimeout(1000);

  // Accept cookies if present
  const btn = page.locator('button:has-text("قبول ومتابعة")');
  if (await btn.isVisible()) {
    await btn.click();
    await page.waitForTimeout(300);
  }

  // 1. Check counts
  const counts = await page.evaluate(() => {
    return {
      all: document.getElementById('cntAll')?.innerText,
      falso: document.getElementById('cntFalso')?.innerText,
      vero: document.getElementById('cntVero')?.innerText,
      exc: document.getElementById('cntExc')?.innerText,
      cardsCount: document.querySelectorAll('.ps-card').length,
      statWords: document.getElementById('statWordsCount')?.innerText,
      statQuestions: document.getElementById('statQuestionsCovered')?.innerText
    };
  });
  console.log('Counts on Page:', counts);

  // 2. Check filters row geometry (Horizontal scroll check)
  const filtersRowGeometry = await page.evaluate(() => {
    const row = document.querySelector('.ps-filters-row');
    const btns = Array.from(document.querySelectorAll('.ps-filter-btn')).map(b => ({
      text: b.innerText,
      rect: b.getBoundingClientRect()
    }));
    return {
      scrollWidth: row.scrollWidth,
      clientWidth: row.clientWidth,
      hasHorizontalScroll: row.scrollWidth > row.clientWidth,
      buttonsCount: btns.length,
      firstBtnLeft: btns[0]?.rect.left,
      lastBtnRight: btns[btns.length - 1]?.rect.right,
      rowWidth: row.getBoundingClientRect().width
    };
  });
  console.log('Filters Row Geometry:', filtersRowGeometry);

  // 3. Take screenshots of loaded page
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_radar_chips_wrapped_and_loaded.png' });

  // 4. Test filtering
  await page.locator('#btnFilterFalso').click();
  await page.waitForTimeout(300);
  const falsoCardsCount = await page.evaluate(() => document.querySelectorAll('.ps-card').length);
  console.log('FALSO Filter Cards Count:', falsoCardsCount);

  await page.locator('#btnFilterVero').click();
  await page.waitForTimeout(300);
  const veroCardsCount = await page.evaluate(() => document.querySelectorAll('.ps-card').length);
  console.log('VERO Filter Cards Count:', veroCardsCount);

  await browser.close();
  console.log('VERIFICATION FINISHED SUCCESSFULLY!');
})();
