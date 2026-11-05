import asyncio
import os
from playwright.async_api import async_playwright

async def capture():
    artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
    os.makedirs(artifact_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 1500})
        await page.goto('http://localhost:8080/tools/icon_proposals_live.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        out_path = os.path.join(artifact_dir, 'icon_proposals_live.png')
        await page.screenshot(path=out_path, full_page=True)
        print(f'SUCCESS: Screenshot saved to {out_path}')

        # Also capture individual closeups of proposal 1 & 2
        p1 = await page.query_selector('.proposal-card:nth-child(1)')
        if p1:
            await p1.screenshot(path=os.path.join(artifact_dir, 'proposal_1_closeup.png'))
            
        p2 = await page.query_selector('.proposal-card:nth-child(2)')
        if p2:
            await p2.screenshot(path=os.path.join(artifact_dir, 'proposal_2_closeup.png'))

        p3 = await page.query_selector('.proposal-card:nth-child(3)')
        if p3:
            await p3.screenshot(path=os.path.join(artifact_dir, 'proposal_3_closeup.png'))

        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture())
