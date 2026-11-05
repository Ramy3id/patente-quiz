import asyncio
import os
from playwright.async_api import async_playwright

async def capture():
    artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
    os.makedirs(artifact_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 1600})
        await page.goto('http://localhost:8080/tools/radical_icon_types_showcase.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        out_path = os.path.join(artifact_dir, 'radical_icon_types_showcase.png')
        await page.screenshot(path=out_path, full_page=True)
        print(f'SUCCESS: Screenshot saved to {out_path}')

        # Snap individual cards for carousel
        c0 = await page.query_selector('.family-card:nth-child(1)')
        if c0: await c0.screenshot(path=os.path.join(artifact_dir, 'family_0_current.png'))

        c1 = await page.query_selector('.family-card:nth-child(2)')
        if c1: await c1.screenshot(path=os.path.join(artifact_dir, 'family_1_3d_clay.png'))

        c2 = await page.query_selector('.family-card:nth-child(3)')
        if c2: await c2.screenshot(path=os.path.join(artifact_dir, 'family_2_flat_vector.png'))

        c3 = await page.query_selector('.family-card:nth-child(4)')
        if c3: await c3.screenshot(path=os.path.join(artifact_dir, 'family_3_neon_glow.png'))

        c4 = await page.query_selector('.family-card:nth-child(5)')
        if c4: await c4.screenshot(path=os.path.join(artifact_dir, 'family_4_glass.png'))

        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture())
