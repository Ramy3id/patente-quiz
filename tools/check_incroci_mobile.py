import asyncio
import io
import sys
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 375, 'height': 812})
        url = 'http://localhost:8080/interactive_pages/decodificatore-incroci.html'
        await page.goto(url, wait_until='domcontentloaded')
        await page.evaluate("""() => {
            localStorage.setItem('patente_gdpr_consent', 'accepted');
        }""")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(800)

        # Scroll to sim section
        sim_header = await page.query_selector('.sim-nav-header')
        if sim_header:
            await sim_header.scroll_into_view_if_needed()
            await page.wait_for_timeout(400)
            await page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\incroci_sim_nav_current.png')
            print("Captured incroci_sim_nav_current.png")

        # Also screenshot the simulation card
        sim_card = await page.query_selector('.simulator-card')
        if sim_card:
            await sim_card.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\incroci_sim_card.png')
            print("Captured incroci_sim_card.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())
