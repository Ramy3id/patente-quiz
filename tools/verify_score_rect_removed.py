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
        
        url = 'http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html'
        await page.goto(url, wait_until='domcontentloaded')
        await page.evaluate("""() => {
            localStorage.setItem('patente_gdpr_consent', 'accepted');
        }""")
        await page.reload(wait_until='networkidle')
        await page.wait_for_selector('.score-strip')
        
        # Test Light Mode
        await page.evaluate("""() => {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }""")
        await page.wait_for_timeout(400)
        
        styles_light = await page.evaluate("""() => {
            const strip = document.querySelector('.score-strip');
            const cs = window.getComputedStyle(strip);
            const cells = Array.from(document.querySelectorAll('.score-cell')).map(c => {
                const s = window.getComputedStyle(c);
                return {
                    border: s.border,
                    borderRadius: s.borderRadius,
                    bg: s.backgroundColor
                };
            });
            return {
                strip_border: cs.border,
                strip_border_width: cs.borderWidth,
                strip_bg: cs.backgroundColor,
                strip_box_shadow: cs.boxShadow,
                cells: cells
            };
        }""")
        print('LIGHT MODE STYLES:')
        print(styles_light)
        
        header = await page.query_selector('.ch-header-card')
        if header:
            await header.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_score_no_rect_light.png')
            print('Captured verified_score_no_rect_light.png')
            
        # Test Dark Mode
        await page.evaluate("""() => {
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
        }""")
        await page.wait_for_timeout(400)
        
        styles_dark = await page.evaluate("""() => {
            const strip = document.querySelector('.score-strip');
            const cs = window.getComputedStyle(strip);
            return {
                strip_border: cs.border,
                strip_border_width: cs.borderWidth,
                strip_bg: cs.backgroundColor,
                strip_box_shadow: cs.boxShadow
            };
        }""")
        print('DARK MODE STYLES:')
        print(styles_dark)
        
        if header:
            await header.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_score_no_rect_dark.png')
            print('Captured verified_score_no_rect_dark.png')
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
