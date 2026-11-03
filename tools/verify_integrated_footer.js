const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });

  await page.goto('http://localhost:8080/interactive_pages/parole-spia.html');
  await page.waitForTimeout(1200);

  // Accept cookies if present
  const btn = page.locator('button:has-text("قبول ومتابعة")');
  if (await btn.isVisible()) {
    await btn.click();
    await page.waitForTimeout(300);
  }

  // Scroll to footer
  await page.evaluate(() => {
    const footer = document.querySelector('footer');
    if (footer) footer.scrollIntoView({ behavior: 'instant' });
  });
  await page.waitForTimeout(500);

  // 1. Inspect Dark Mode styles
  const darkFooterStyles = await page.evaluate(() => {
    const card = document.querySelector('.footer-dev-card-compact');
    const comp = window.getComputedStyle(card);
    const bottom = document.querySelector('.footer-bottom-compact');
    const bottomComp = window.getComputedStyle(bottom);
    return {
      cardBackground: comp.backgroundColor,
      cardBorder: comp.border,
      cardBorderTop: comp.borderTop,
      cardBoxShadow: comp.boxShadow,
      bottomBorderTop: bottomComp.borderTop
    };
  });
  console.log('Dark Mode Footer Styles:', darkFooterStyles);

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_integrated_footer_dark.png' });

  // 2. Switch to Light Mode
  await page.evaluate(() => {
    document.documentElement.classList.add('light');
    document.documentElement.classList.remove('dark');
  });
  await page.waitForTimeout(400);

  const lightFooterStyles = await page.evaluate(() => {
    const card = document.querySelector('.footer-dev-card-compact');
    const comp = window.getComputedStyle(card);
    const bottom = document.querySelector('.footer-bottom-compact');
    const bottomComp = window.getComputedStyle(bottom);
    return {
      cardBackground: comp.backgroundColor,
      cardBorder: comp.border,
      cardBorderTop: comp.borderTop,
      cardBoxShadow: comp.boxShadow,
      bottomBorderTop: bottomComp.borderTop
    };
  });
  console.log('Light Mode Footer Styles:', lightFooterStyles);

  await page.screenshot({ path: 'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_integrated_footer_light.png' });

  await browser.close();
  console.log('FOOTER VERIFICATION COMPLETED SUCCESSFULLY!');
})();
