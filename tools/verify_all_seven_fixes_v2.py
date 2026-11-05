import asyncio
import os
from playwright.async_api import async_playwright

async def verify():
    artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
    os.makedirs(artifact_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # 1. Mobile View - Dark Mode
        context_mobile = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15'
        )
        page = await context_mobile.new_page()
        
        # Pre-set cookie consent to avoid popup
        await page.add_init_script("""
            localStorage.setItem('patente_cookie_consent', 'accepted');
            localStorage.setItem('cookieConsentAccepted', 'true');
        """)
        
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        # Close banner if still appears
        btn_consent = await page.query_selector('.btn-cookie-accept, button:has-text("قبول ومتابعة")')
        if btn_consent:
            await btn_consent.click()
            await page.wait_for_timeout(300)

        # Snap Bento tools and Chapter 1 (Image 7 comparison)
        await page.screenshot(
            path=os.path.join(artifact_dir, 'v2_mobile_bento_and_ch1.png'),
            clip={'x': 0, 'y': 220, 'width': 390, 'height': 750}
        )

        # Scroll to footer brand (Image 1, 5 comparison)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(600)
        await page.screenshot(
            path=os.path.join(artifact_dir, 'v2_mobile_footer_and_dock.png')
        )

        # Open Spotlight Search modal (Image 2 comparison)
        await page.click('#btnOpenMobileSearch')
        await page.wait_for_selector('#globalSearchModal', state='visible')
        await page.wait_for_timeout(500)
        await page.screenshot(
            path=os.path.join(artifact_dir, 'v2_mobile_search_clean.png')
        )

        # Close search
        await page.click('#btnCloseGlobalSearch')
        await page.wait_for_timeout(300)

        # 2. Desktop View - Light Mode
        context_desktop = await browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        page_desk = await context_desktop.new_page()
        await page_desk.add_init_script("""
            localStorage.setItem('patente_cookie_consent', 'accepted');
            localStorage.setItem('cookieConsentAccepted', 'true');
        """)
        await page_desk.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        
        # Set light mode via JS
        await page_desk.evaluate("document.documentElement.classList.add('light')")
        await page_desk.wait_for_timeout(400)

        # Dismiss cookie if exists
        btn_c = await page_desk.query_selector('.btn-cookie-accept, button:has-text("قبول ومتابعة")')
        if btn_c:
            await btn_c.click()
            await page_desk.wait_for_timeout(300)

        # Desktop Footer in Light Mode
        await page_desk.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page_desk.wait_for_timeout(600)
        await page_desk.screenshot(
            path=os.path.join(artifact_dir, 'v2_desktop_footer_light.png')
        )

        await browser.close()
        print('SUCCESS: All v2 verification screenshots captured cleanly!')

if __name__ == '__main__':
    asyncio.run(verify())
