import asyncio
from playwright.async_api import async_playwright

async def measure_actual_widths():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        pages = [
            ('Capitoli Home', 'http://localhost:8080/Capitoli_Divisi/index.html', '.container'),
            ('Capitolo 01', 'http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html', '.container'),
            ('Capitolo 13', 'http://localhost:8080/Capitoli_Divisi/Capitolo_13_norme_di_circolazione/index.html', '.container'),
            ('Dizionario Sinonimi', 'http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html', '.container'),
            ('Parole Quiz', 'http://localhost:8080/Capitoli_Divisi/parole-quiz.html', '.container'),
            ('Piano Studio', 'http://localhost:8080/interactive_pages/piano-studio.html', '.sp-container'),
            ('Scheda Esame', 'http://localhost:8080/interactive_pages/scheda-esame.html', '.exam-portal-container'),
            ('Decodificatore Incroci', 'http://localhost:8080/interactive_pages/decodificatore-incroci.html', '.inc-container')
        ]
        
        results = []
        for name, url, sel in pages:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(300)
            data = await page.evaluate('''sel => {
                const el = document.querySelector(sel);
                if (!el) return { width: 0, maxWidth: 'none', found: false };
                const cs = window.getComputedStyle(el);
                return {
                    width: el.getBoundingClientRect().width,
                    maxWidth: cs.maxWidth,
                    found: true
                };
            }''', sel)
            results.append((name, data))
            
            slug = name.lower().replace(' ', '_')
            await page.screenshot(path=rf'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/live1200_{slug}.png')
            
        await browser.close()
        
        print("="*60)
        print("VERIFIED LIVE RENDERED CONTAINER WIDTHS (DESKTOP 1440px)")
        print("="*60)
        for name, d in results:
            print(f"{name:<25} | maxWidth: {d['maxWidth']:<10} | rendered width: {d['width']}px")
        print("="*60)

asyncio.run(measure_actual_widths())
