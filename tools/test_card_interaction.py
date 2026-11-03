import asyncio
import io
import sys
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def test_interaction():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 375, 'height': 812})
        page = await context.new_page()

        url = 'http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html'
        await page.goto(url, wait_until='domcontentloaded')
        await page.evaluate("""() => {
            localStorage.setItem('patente_gdpr_consent', 'accepted');
        }""")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(500)

        # Expand sections
        await page.evaluate("""() => {
            if (typeof expandAllSections === 'function') expandAllSections();
            const nav = document.getElementById('unifiedNavBar');
            if (nav) nav.style.display = 'none';
        }""")
        await page.wait_for_timeout(400)

        # Click VERO on first card
        btn_v = await page.query_selector('.q-card .btn-ans-v')
        if btn_v:
            await btn_v.click()
            await page.wait_for_timeout(300)

        # Click explain drawer on first card
        btn_exp = await page.query_selector('.q-card .btn-explain-toggle')
        if btn_exp:
            await btn_exp.click()
            await page.wait_for_timeout(300)

        card = await page.query_selector('.q-card')
        if card:
            await card.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_card_answered_drawer.png')
            print("Captured verified_card_answered_drawer.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_interaction())
