import asyncio
import io
import sys
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 375, 'height': 812})
        page = await context.new_page()

        url = 'http://localhost:8080/interactive_pages/decodificatore-incroci.html'
        await page.goto(url, wait_until='domcontentloaded')
        await page.evaluate("""() => {
            localStorage.setItem('patente_gdpr_consent', 'accepted');
        }""")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(600)

        # LIGHT MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
            // Hide bottom nav for screenshots
            const nav = document.getElementById('unifiedNavBar');
            if (nav) nav.style.display = 'none';
            const btt = document.getElementById('btnBackToTop');
            if (btt) btt.style.display = 'none';
            document.querySelectorAll('.back-to-top, .scroll-top-btn').forEach(el => el.style.display = 'none');
        }""")
        await page.wait_for_timeout(400)

        # Check scroll width
        scroll_info = await page.evaluate("""() => {
            return {
                docScrollWidth: document.documentElement.scrollWidth,
                docClientWidth: document.documentElement.clientWidth,
                hasHorizScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth
            };
        }""")
        print("SCROLL INFO LIGHT:", scroll_info)

        # Check navigation header box
        sim_header = await page.query_selector('.sim-nav-header')
        if sim_header:
            await sim_header.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)
            await sim_header.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_incroci_nav_light.png')
            print("Captured verified_incroci_nav_light.png")

        sim_section = await page.query_selector('.traffic-sim-section')
        if sim_section:
            await sim_section.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_incroci_sim_card_light.png')
            print("Captured verified_incroci_sim_card_light.png")

        # DARK MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
        }""")
        await page.wait_for_timeout(400)

        if sim_header:
            await sim_header.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_incroci_nav_dark.png')
            print("Captured verified_incroci_nav_dark.png")

        if sim_section:
            await sim_section.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_incroci_sim_card_dark.png')
            print("Captured verified_incroci_sim_card_dark.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
