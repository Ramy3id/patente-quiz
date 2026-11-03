const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html');
  const btn = page.locator('button:has-text("قبول ومتابعة")');
  if (await btn.isVisible()) {
    await btn.click();
    await page.waitForTimeout(300);
  }

  // Click VERO on Q1
  await page.locator('.choice-btn-vero').click();
  await page.waitForTimeout(350);

  // Click FALSO on Q2
  await page.locator('.choice-btn-falso').click();
  await page.waitForTimeout(350);

  // Now we should be on Q3
  let textQ3 = await page.locator('.exam-q-badge').textContent();
  console.log('Current after 2 answers:', textQ3.trim());

  // Click Previous button (#btnPrev)
  await page.locator('#btnPrev').click();
  await page.waitForTimeout(100);

  let textQ2 = await page.locator('.exam-q-badge').textContent();
  console.log('After clicking Previous:', textQ2.trim());

  // Check that FALSO is still selected on Q2
  const falsoSelected = await page.locator('.choice-btn-falso.selected').isVisible();
  console.log('Q2 FALSO is selected:', falsoSelected);

  // Tap pill 1 directly
  await page.locator('.q-pill[data-idx="0"]').click();
  await page.waitForTimeout(100);
  let textQ1 = await page.locator('.exam-q-badge').textContent();
  console.log('After tapping pill 1:', textQ1.trim());

  const veroSelected = await page.locator('.choice-btn-vero.selected').isVisible();
  console.log('Q1 VERO is selected:', veroSelected);

  await browser.close();
  console.log('All navigation verification complete.');
})();
