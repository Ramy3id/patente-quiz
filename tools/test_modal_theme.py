import asyncio
import io
import sys
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def test_modal():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 375, 'height': 812})
        page = await context.new_page()

        url = 'http://localhost:8080/interactive_pages/decodificatore-incroci.html'
        await page.goto(url, wait_until='domcontentloaded')
        
        # Check initial theme
        init_theme = await page.evaluate("() => ({ class: document.documentElement.className, localTheme: localStorage.getItem('patente_theme') })")
        print("Initial theme:", init_theme)

        # Set light theme explicitly
        await page.evaluate("""() => {
            if (window.applyTheme) window.applyTheme('light');
            else {
                document.documentElement.classList.remove('dark');
                document.documentElement.classList.add('light');
            }
        }""")
        await page.wait_for_timeout(300)

        # Open Figure Modal
        await page.evaluate("() => openFigureModal()")
        await page.wait_for_timeout(500)

        # Check modal computed styles
        modal_styles = await page.evaluate("""() => {
            const card = document.querySelector('.fig-modal-card');
            const search = document.querySelector('.fig-modal-search');
            const closeBtn = document.querySelector('.fig-modal-close');
            return {
                card_bg: card ? window.getComputedStyle(card).backgroundColor : null,
                card_border: card ? window.getComputedStyle(card).borderColor : null,
                search_bg: search ? window.getComputedStyle(search).backgroundColor : null,
                search_color: search ? window.getComputedStyle(search).color : null,
                close_width: closeBtn ? window.getComputedStyle(closeBtn).width : null,
                close_height: closeBtn ? window.getComputedStyle(closeBtn).height : null,
                close_border_radius: closeBtn ? window.getComputedStyle(closeBtn).borderRadius : null
            };
        }""")
        print("MODAL STYLES IN LIGHT MODE:")
        print(modal_styles)

        # Take screenshot of open modal
        await page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\debug_modal_light.png')
        print("Captured debug_modal_light.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_modal())
