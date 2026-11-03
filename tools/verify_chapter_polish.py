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
        await page.wait_for_timeout(800)

        # 1. LIGHT MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }""")
        await page.wait_for_timeout(400)

        # Inspect Search Box width
        search_box = await page.query_selector('#q-search')
        sb_box = await search_box.bounding_box() if search_box else None
        print("Search Box width:", sb_box['width'] if sb_box else 'None')

        # Inspect Grouped Mode Button text
        btn_mode = await page.query_selector('#btn-mode-grouped')
        btn_text = await btn_mode.inner_text() if btn_mode else 'None'
        print("View mode button text:", btn_text.replace('\n', ' '))

        # Inspect Subtopic Stats Header
        subtopic_stats = await page.query_selector('.subtopic-header-stats')
        if subtopic_stats:
            cs = await page.evaluate("(el) => window.getComputedStyle(el).justifyContent", subtopic_stats)
            print("Subtopic stats justifyContent:", cs)

        # Capture Screenshot 1: Hub (with قوائم مقسمة & centered تصفير الإنجاز) (Light)
        hub = await page.query_selector('#subtopics-hub-card')
        if hub:
            await hub.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_hub_light.png')
            print("Captured verified_hub_light.png")

        # Capture Screenshot 2: Controls Bar with full width search box (Light)
        controls = await page.query_selector('.controls-bar')
        if controls:
            await controls.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_controls_light.png')
            print("Captured verified_controls_light.png")

        # Capture Screenshot 3: Subtopic Section Header with centered 3 stats (Light)
        sub_header = await page.query_selector('.subtopic-section-header')
        if sub_header:
            await sub_header.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_subtopic_stats_light.png')
            print("Captured verified_subtopic_stats_light.png")

        # Expand sections so questions become visible
        await page.evaluate("""() => {
            if (typeof expandAllSections === 'function') {
                expandAllSections();
            }
        }""")
        await page.wait_for_timeout(600)

        # Inspect Question Card Answer Grid
        ans_grid = await page.query_selector('.q-answers-grid')
        if ans_grid:
            grid_cols = await page.evaluate("(el) => window.getComputedStyle(el).gridTemplateColumns", ans_grid)
            print("Answer grid columns:", grid_cols)

        # Find first question card with an image
        q_cards = await page.query_selector_all('.q-card')
        q_card_target = None
        for qc in q_cards:
            img = await qc.query_selector('.q-img-wrap img')
            if img:
                q_card_target = qc
                break
        if not q_card_target and len(q_cards) > 0:
            q_card_target = q_cards[0]

        # Capture Screenshot 4: Question Card (Light)
        if q_card_target:
            await q_card_target.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)
            await q_card_target.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_question_card_light.png')
            print("Captured verified_question_card_light.png")

        # 2. DARK MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
        }""")
        await page.wait_for_timeout(400)

        if controls:
            await controls.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_controls_dark.png')
            print("Captured verified_controls_dark.png")

        if sub_header:
            await sub_header.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_subtopic_stats_dark.png')
            print("Captured verified_subtopic_stats_dark.png")

        if q_card_target:
            await q_card_target.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)
            await q_card_target.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_question_card_dark.png')
            print("Captured verified_question_card_dark.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
