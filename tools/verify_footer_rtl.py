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

        # 1. LIGHT MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }""")
        await page.wait_for_timeout(300)

        # Check footer computed styles
        footer_info = await page.evaluate("""() => {
            const footer = document.querySelector('.unified-portal-footer');
            const desc = document.querySelector('.footer-brand-desc');
            const title = document.querySelector('.footer-col-title');
            const link = document.querySelector('.footer-nav-link');
            const cs = window.getComputedStyle(footer);
            const csDesc = desc ? window.getComputedStyle(desc) : {};
            const csTitle = title ? window.getComputedStyle(title) : {};
            const csLink = link ? window.getComputedStyle(link) : {};
            return {
                footer_dir: cs.direction,
                footer_align: cs.textAlign,
                desc_align: csDesc.textAlign,
                desc_dir: csDesc.direction,
                title_align: csTitle.textAlign,
                title_dir: csTitle.direction,
                link_align: csLink.textAlign,
                link_dir: csLink.direction
            };
        }""")
        print("FOOTER COMPUTED STYLES:")
        print(footer_info)

        # Scroll to footer
        footer = await page.query_selector('.unified-portal-footer')
        if footer:
            await footer.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)
            
            # Hide bottom nav so it doesn't cover footer screenshot
            await page.evaluate("""() => {
                const nav = document.getElementById('unifiedNavBar');
                if (nav) nav.style.display = 'none';
                const btt = document.getElementById('btnBackToTop');
                if (btt) btt.style.display = 'none';
                document.querySelectorAll('.back-to-top, .scroll-top-btn').forEach(el => el.style.display = 'none');
            }""")
            await page.wait_for_timeout(200)

            # Capture screenshot matching user's view (top part of footer)
            top_grid = await page.query_selector('.footer-top-grid')
            if top_grid:
                await top_grid.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_footer_rtl_light.png')
                print("Captured verified_footer_rtl_light.png")

        # 2. DARK MODE
        await page.evaluate("""() => {
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
        }""")
        await page.wait_for_timeout(300)

        if top_grid:
            await top_grid.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_footer_rtl_dark.png')
            print("Captured verified_footer_rtl_dark.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
