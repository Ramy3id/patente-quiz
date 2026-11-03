const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const viewports = [
    { name: 'Android Galaxy (360x740)', w: 360, h: 740 },
    { name: 'iPhone 13 (390x844)', w: 390, h: 844 },
    { name: 'Pixel 7 (412x915)', w: 412, h: 915 }
  ];

  for (const vp of viewports) {
    const page = await browser.newPage({ viewport: { width: vp.w, height: vp.h } });
    await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
    await page.waitForTimeout(600);

    const positions = await page.evaluate(() => {
      const hub = document.getElementById('examMasterControlHub');
      const sw = document.getElementById('masterSkinSwitcher');
      const timer = document.getElementById('examTimerDisplay');
      const prog = document.querySelector('.hub-progress-badge');
      const pills = document.getElementById('examPillsGrid');
      const pill1 = document.querySelector('.q-pill');
      const card = document.getElementById('questionCardStage');

      return {
        hubR: hub.getBoundingClientRect(),
        swR: sw.getBoundingClientRect(),
        timerR: timer.getBoundingClientRect(),
        progR: prog.getBoundingClientRect(),
        pillsR: pills.getBoundingClientRect(),
        pill1R: pill1 ? pill1.getBoundingClientRect() : null,
        cardR: card.getBoundingClientRect(),
        pill1OverlapsSwitcher: pill1 ? (pill1.getBoundingClientRect().top < sw.getBoundingClientRect().bottom) : false,
        overlapAmount: pill1 ? (sw.getBoundingClientRect().bottom - pill1.getBoundingClientRect().top) : 0
      };
    });

    console.log(vp.name, '=> Overlap:', positions.pill1OverlapsSwitcher, 'Amount:', positions.overlapAmount);
    await page.screenshot({ path: `C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/vp_${vp.w}.png` });
    await page.close();
  }

  await browser.close();
})();
