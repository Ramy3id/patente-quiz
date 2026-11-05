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
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # Snap Bento tools and Chapter 1 (Image 7 comparison)
        await page.screenshot(
            path=os.path.join(artifact_dir, 'verification_mobile_bento_cards.png'),
            clip={'x': 0, 'y': 250, 'width': 390, 'height': 900}
        )

        # Scroll to bottom to capture Footer and Dock (Image 1, 3, 5, 6 comparison)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(600)
        await page.screenshot(
            path=os.path.join(artifact_dir, 'verification_mobile_footer_dock.png')
        )

        # Open Spotlight Search modal (Image 2 comparison)
        await page.click('#btnOpenMobileSearch')
        await page.wait_for_selector('#globalSearchModal', state='visible')
        await page.wait_for_timeout(600)
        await page.screenshot(
            path=os.path.join(artifact_dir, 'verification_mobile_search_modal.png')
        )

        # 2. Desktop View - Light Mode
        context_desktop = await browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        page_desk = await context_desktop.new_page()
        await page_desk.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        
        # Switch to light mode
        await page_desk.click('#themeTogglePortalBtn')
        await page_desk.wait_for_timeout(500)

        # Open search on desktop
        await page_desk.keyboard.press('Control+k')
        await page_desk.wait_for_selector('#globalSearchModal', state='visible')
        await page_desk.wait_for_timeout(600)
        await page_desk.screenshot(
            path=os.path.join(artifact_dir, 'verification_desktop_search_light.png')
        )

        # Close search
        await page_desk.keyboard.press('Escape')
        await page_desk.wait_for_timeout(300)

        # Scroll to footer on desktop
        await page_desk.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page_desk.wait_for_timeout(600)
        await page_desk.screenshot(
            path=os.path.join(artifact_dir, 'verification_desktop_footer_light.png')
        )

        await browser.close()
        print('SUCCESS: All 5 verification screenshots captured!')

if __name__ == '__main__':
    asyncio.run(verify())
