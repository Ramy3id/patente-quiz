import asyncio
import os
from playwright.async_api import async_playwright

async def verify():
    artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.add_init_script("localStorage.setItem('cookieConsentAccepted', 'true');")
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        # Scroll to .footer-col-brand
        brand_col = await page.query_selector('.footer-col-brand')
        if brand_col:
            await brand_col.scroll_into_view_if_needed()
            await page.wait_for_timeout(400)
            await brand_col.screenshot(path=os.path.join(artifact_dir, 'v2_mobile_footer_brand_col.png'))
            print('SUCCESS: Captured brand column!')

        # Also capture desktop footer brand header
        page_desk = await browser.new_page(viewport={'width': 1280, 'height': 800})
        await page_desk.add_init_script("localStorage.setItem('cookieConsentAccepted', 'true');")
        await page_desk.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        await page_desk.evaluate("document.documentElement.classList.add('light')")
        await page_desk.wait_for_timeout(400)
        desk_brand = await page_desk.query_selector('.footer-col-brand')
        if desk_brand:
            await desk_brand.scroll_into_view_if_needed()
            await page_desk.wait_for_timeout(400)
            await desk_brand.screenshot(path=os.path.join(artifact_dir, 'v2_desktop_footer_brand_col_light.png'))
            print('SUCCESS: Captured desktop brand column light!')

        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
