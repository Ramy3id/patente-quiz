const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/Capitoli_Divisi/index.html');

  const items = [
    { cat: 'all', title: 'الكل', sub: '25 باباً' },
    { cat: 'segnali', title: 'الإشارات', sub: '02-10' },
    { cat: 'norme', title: 'القواعد', sub: '11-13' },
    { cat: 'precedenze', title: 'التقاطعات', sub: '14-16' },
    { cat: 'sicurezza', title: 'السلامة', sub: '17-20' },
    { cat: 'meccanica', title: 'الميكانيكا', sub: '21-25' }
  ];

  const results = await page.evaluate((items) => {
    const chips = Array.from(document.querySelectorAll('.chip-btn'));
    return chips.map((b, i) => {
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
      b.style.height = '44px';

      const tEl = b.querySelector('.chip-title');
      tEl.style.fontSize = '0.78rem';
      tEl.style.fontWeight = '700';

      const sEl = b.querySelector('.chip-sub');
      sEl.style.fontSize = '0.65rem';
      sEl.style.opacity = '0.75';
      sEl.style.fontFamily = 'monospace';

      return {
        title: items[i].title,
        scrollWidth: b.scrollWidth,
        clientWidth: b.clientWidth,
        isCutOff: b.scrollWidth > b.clientWidth
      };
    });
  }, items);

  console.log('Tested 2-tier chip labels on 375px:');
  console.table(results);

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_chips_2tier.png' });
  console.log('Saved screenshot to verified_chips_2tier.png');

  await browser.close();
})();
