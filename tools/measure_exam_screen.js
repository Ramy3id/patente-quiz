const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  const acceptBtn = await page.$('button:has-text("قبول ومتابعة")');
  if (acceptBtn) await acceptBtn.click();
  await page.waitForTimeout(300);

  const measurements = await page.evaluate(() => {
    const nav = document.getElementById('globalPortalNav');
    const switcher = document.querySelector('.exam-skin-switcher');
    const topBar = document.querySelector('.exam-top-bar');
    const pills = document.getElementById('examPillsGrid');
    const stage = document.getElementById('questionCardStage');
    const submit = document.getElementById('btnSubmitFinalExam');
    const dock = document.getElementById('nativeBottomDock');
    return {
      windowHeight: window.innerHeight,
      documentHeight: document.documentElement.scrollHeight,
      overflow: document.documentElement.scrollHeight - window.innerHeight,
      nav: nav ? Math.round(nav.getBoundingClientRect().height) : 0,
      switcher: switcher ? Math.round(switcher.getBoundingClientRect().height) : 0,
      topBar: topBar ? Math.round(topBar.getBoundingClientRect().height) : 0,
      pills: pills ? Math.round(pills.getBoundingClientRect().height) : 0,
      stage: stage ? Math.round(stage.getBoundingClientRect().height) : 0,
      submit: submit ? Math.round(submit.getBoundingClientRect().height) : 0,
      dock: dock ? Math.round(dock.getBoundingClientRect().height) : 0
    };
  });
  console.log('Current measurements:', measurements);
  await browser.close();
})();
