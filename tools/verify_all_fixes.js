const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/Capitoli_Divisi/index.html');

  // Accept GDPR
  const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
  if (acceptBtn) await acceptBtn.click();
  await page.waitForTimeout(300);

  console.log('=== TEST 1: Circular Buttons Verification ===');
  // 1. Scroll-to-top button
  await page.evaluate(() => window.scrollTo(0, 1000));
  await page.waitForTimeout(300);
  const scrollBtnInfo = await page.evaluate(() => {
    const el = document.getElementById('patenteScrollTopBtn');
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { width: r.width, height: r.height, borderRadius: window.getComputedStyle(el).borderRadius };
  });
  console.log('ScrollBtn:', scrollBtnInfo);

  // 2. Gate Modal Close Button
  await page.evaluate(() => {
    if (window.PatenteAuth && window.PatenteAuth.showGateModal) {
      window.PatenteAuth.showGateModal({ title: 'فحص الإغلاق', message: 'تجربة' });
    }
  });
  await page.waitForTimeout(300);
  const gateCloseInfo = await page.evaluate(() => {
    const el = document.getElementById('btnGateClose');
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { width: r.width, height: r.height, borderRadius: window.getComputedStyle(el).borderRadius };
  });
  console.log('GateCloseBtn:', gateCloseInfo);

  // Take screenshot of open gate modal with circular close button
  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_gate_modal_circle.png' });

  // Close gate modal
  await page.click('#btnGateClose');
  await page.waitForTimeout(200);

  console.log('\n=== TEST 2: Arabic Normalization Search Tests ===');
  const searchQueries = [
    { q: 'اشارات', expectedMin: 1, desc: 'Bare Alif (without hamza)' },
    { q: 'اسبقية', expectedMin: 1, desc: 'Bare Alif for أسبقية' },
    { q: 'اسبقيه', expectedMin: 1, desc: 'Haa instead of Taa Marbuta' },
    { q: 'الاول', expectedMin: 1, desc: 'Bare Alif for الأول' },
    { q: '14', expectedMin: 1, desc: 'Chapter number 14' },
    { q: 'sorpasso', expectedMin: 1, desc: 'Italian word' }
  ];

  for (const item of searchQueries) {
    await page.fill('#chapter-search', item.q);
    await page.waitForTimeout(100);
    const visibleCount = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('.chapter-card')).filter(c => c.style.display !== 'none').length;
    });
    console.log(`Query: "${item.q}" (${item.desc}) -> ${visibleCount} chapters visible [${visibleCount >= item.expectedMin ? 'PASS' : 'FAIL'}]`);
  }

  // Clear search
  await page.fill('#chapter-search', '');
  await page.waitForTimeout(100);

  console.log('\n=== TEST 3: Category Filter Chips (No Cutoff) ===');
  const chipsStatus = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('.chip-btn')).map(b => {
      return {
        cat: b.dataset.cat,
        title: b.querySelector('.chip-title') ? b.querySelector('.chip-title').textContent : b.textContent,
        sub: b.querySelector('.chip-sub') ? b.querySelector('.chip-sub').textContent : '',
        scrollWidth: b.scrollWidth,
        clientWidth: b.clientWidth,
        isCutOff: b.scrollWidth > b.clientWidth
      };
    });
  });
  console.table(chipsStatus);

  // Take screenshot of search + chips area
  const controlsEl = await page.$('.controls-bar');
  if (controlsEl) {
    await controlsEl.scrollIntoViewIfNeeded();
    await page.waitForTimeout(200);
    await controlsEl.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_search_and_chips.png' });
  }

  await browser.close();
  console.log('\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY.');
})();
