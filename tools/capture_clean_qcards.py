import asyncio
import io
import sys
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def run():
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
        await page.wait_for_timeout(600)

        # Expand sections
        await page.evaluate("""() => {
            if (typeof expandAllSections === 'function') expandAllSections();
            // Hide bottom nav and scroll to top button so they don't overlay the card screenshot
            const nav = document.getElementById('unifiedNavBar');
            if (nav) nav.style.display = 'none';
            const btt = document.getElementById('btnBackToTop');
            if (btt) btt.style.display = 'none';
            document.querySelectorAll('.back-to-top, .scroll-top-btn').forEach(el => el.style.display = 'none');
        }""")
        await page.wait_for_timeout(400)

        # LIGHT MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }""")
        await page.wait_for_timeout(300)

        q_cards = await page.query_selector_all('.q-card')
        q_card_target = None
        for qc in q_cards:
            img = await qc.query_selector('.q-img-wrap img')
            if img:
                q_card_target = qc
                break
        if not q_card_target and len(q_cards) > 0:
            q_card_target = q_cards[0]

        if q_card_target:
            await q_card_target.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_question_card_light.png')
            print("Updated verified_question_card_light.png")

        # DARK MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
        }""")
        await page.wait_for_timeout(300)

        if q_card_target:
            await q_card_target.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_question_card_dark.png')
            print("Updated verified_question_card_dark.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
