const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  await page.waitForTimeout(600);

  const overlapData = await page.evaluate(() => {
    const hub = document.getElementById('examMasterControlHub');
    const row = document.querySelector('.hub-primary-row');
    const switcher = document.getElementById('masterSkinSwitcher');
    const pillsRow = document.querySelector('.exam-nav-pills-row');
    const pillsGrid = document.getElementById('examPillsGrid');
    const pill1 = document.querySelector('.q-pill');

    const hubR = hub.getBoundingClientRect();
    const rowR = row.getBoundingClientRect();
    const swR = switcher.getBoundingClientRect();
    const pRowR = pillsRow ? pillsRow.getBoundingClientRect() : null;
    const pGridR = pillsGrid ? pillsGrid.getBoundingClientRect() : null;
    const p1R = pill1 ? pill1.getBoundingClientRect() : null;

    return {
      hub: { top: hubR.top, bottom: hubR.bottom, height: hubR.height },
      row: { top: rowR.top, bottom: rowR.bottom, height: rowR.height },
      switcher: { top: swR.top, bottom: swR.bottom, height: swR.height, left: swR.left, right: swR.right },
      pillsRow: pRowR ? { top: pRowR.top, bottom: pRowR.bottom, height: pRowR.height } : null,
      pillsGrid: pGridR ? { top: pGridR.top, bottom: pGridR.bottom, height: pGridR.height } : null,
      pill1: p1R ? { top: p1R.top, bottom: p1R.bottom, height: p1R.height, left: p1R.left, right: p1R.right } : null,
      overlapY: p1R ? Math.max(0, swR.bottom - p1R.top) : null
    };
  });

  console.log('Overlap Data in Playwright:', JSON.stringify(overlapData, null, 2));

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/diagnose_overlap.png' });
  await browser.close();
})();
