import asyncio
import os
from playwright.async_api import async_playwright

async def verify():
    artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
    os.makedirs(artifact_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 800})
        await page.add_init_script("localStorage.setItem('cookieConsentAccepted', 'true');")
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)

        # Snap the first 3 chapter cards
        card = await page.query_selector('.chapters-grid')
        if card:
            out = os.path.join(artifact_dir, 'verified_chapter_buttons_arrow.png')
            await card.screenshot(path=out)
            print(f"SUCCESS: Captured chapter cards to {out}")

        # Also crop just one button closeup
        btn = await page.query_selector('.btn-action-study')
        if btn:
            out_btn = os.path.join(artifact_dir, 'verified_single_button_arrow.png')
            await btn.screenshot(path=out_btn)
            print(f"SUCCESS: Captured single button to {out_btn}")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
