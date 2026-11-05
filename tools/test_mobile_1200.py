import asyncio
from playwright.async_api import async_playwright

async def test_mobile():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport 390x844
        context = await browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
        page = await context.new_page()
        
        pages = [
            ('Capitoli Home', 'http://localhost:8080/Capitoli_Divisi/index.html'),
            ('Capitolo 01', 'http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html'),
            ('Dizionario Sinonimi', 'http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html'),
            ('Piano Studio', 'http://localhost:8080/interactive_pages/piano-studio.html'),
            ('Scheda Esame', 'http://localhost:8080/interactive_pages/scheda-esame.html')
        ]
        
        print("="*60)
        print("VERIFIED LIVE MOBILE CONTAINER WIDTHS (MOBILE 390px)")
        print("="*60)
        for name, url in pages:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(200)
            data = await page.evaluate('''() => {
                const el = document.querySelector('.container, .sp-container, .inc-container, .exam-portal-container');
                return {
                    scrollWidth: document.documentElement.scrollWidth,
                    clientWidth: document.documentElement.clientWidth,
                    containerWidth: el ? el.getBoundingClientRect().width : 0
                };
            }''')
            overflow = data['scrollWidth'] > data['clientWidth']
            print(f"{name:<25} | container: {data['containerWidth']:.1f}px | overflow: {overflow}")
            
        await browser.close()
        print("="*60)

asyncio.run(test_mobile())
