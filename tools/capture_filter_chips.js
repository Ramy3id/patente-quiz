const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/Capitoli_Divisi/index.html');

  const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
  if (acceptBtn) await acceptBtn.click();
  await page.waitForTimeout(300);

  const items = [
    { cat: 'all', title: 'الكل', sub: '25 باباً' },
    { cat: 'segnali', title: 'الإشارات', sub: '02-10' },
    { cat: 'norme', title: 'القواعد', sub: '11-13' },
    { cat: 'precedenze', title: 'التقاطعات', sub: '14-16' },
    { cat: 'sicurezza', title: 'السلامة', sub: '17-20' },
    { cat: 'meccanica', title: 'الميكانيكا', sub: '21-25' }
  ];

  await page.evaluate((items) => {
    const chips = Array.from(document.querySelectorAll('.chip-btn'));
    chips.forEach((b, i) => {
      b.innerHTML = `
        <span class="chip-title">${items[i].title}</span>
        <span class="chip-sub">${items[i].sub}</span>
      `;
      b.style.display = 'flex';
      b.style.flexDirection = 'column';
      b.style.alignItems = 'center';
      b.style.justifyContent = 'center';
      b.style.gap = '2px';
      b.style.padding = '4px 2px';
      b.style.height = '48px';

      const tEl = b.querySelector('.chip-title');
      tEl.style.fontSize = '0.78rem';
      tEl.style.fontWeight = '700';

      const sEl = b.querySelector('.chip-sub');
      sEl.style.fontSize = '0.64rem';
      sEl.style.opacity = '0.75';
      sEl.style.fontFamily = 'monospace';
    });
  }, items);

  const filterChipsEl = await page.$('.filter-chips');
  if (filterChipsEl) {
    await filterChipsEl.screenshot({
      path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_chips_element.png'
    });
    console.log('Saved filterChipsEl screenshot');
  }

  await browser.close();
})();
