import asyncio
from playwright.async_api import async_playwright

async def measure_widths():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        test_pages = [
            ("capitoli_home", "http://localhost:8080/Capitoli_Divisi/index.html"),
            ("capitolo_01", "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"),
            ("capitolo_13", "http://localhost:8080/Capitoli_Divisi/Capitolo_13_norme_di_circolazione/index.html"),
            ("dizionario", "http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html"),
            ("parole_quiz", "http://localhost:8080/Capitoli_Divisi/parole-quiz.html"),
            ("piano_studio", "http://localhost:8080/interactive_pages/piano-studio.html"),
            ("scheda_esame", "http://localhost:8080/interactive_pages/scheda-esame.html"),
            ("decodificatore", "http://localhost:8080/interactive_pages/decodificatore-incroci.html")
        ]
        
        for name, url in test_pages:
            try:
                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(500)
                
                info = await page.evaluate("""() => {
                    const nav = document.querySelector('#globalPortalNav') || document.querySelector('.unified-portal-nav');
                    const navRect = nav ? nav.getBoundingClientRect() : null;
                    
                    // Main containers
                    const candidates = [
                        document.querySelector('.ch-portal-container'),
                        document.querySelector('.container'),
                        document.querySelector('.portal-container'),
                        document.querySelector('.quiz-container'),
                        document.querySelector('.interactive-container'),
                        document.querySelector('.piano-container'),
                        document.querySelector('.exam-container'),
                        document.querySelector('main'),
                        document.querySelector('.content-wrapper')
                    ].filter(Boolean);
                    
                    const details = candidates.map(el => {
                        const cs = window.getComputedStyle(el);
                        const r = el.getBoundingClientRect();
                        return {
                            tag: el.tagName,
                            className: el.className,
                            id: el.id,
                            width: r.width,
                            maxWidth: cs.maxWidth,
                            paddingLeft: cs.paddingLeft,
                            paddingRight: cs.paddingRight
                        };
                    });
                    
                    return {
                        navWidth: navRect ? navRect.width : 0,
                        containers: details
                    };
                }""")
                print(f"=== {name} ===")
                print(f"  Nav width: {info['navWidth']}")
                for c in info['containers']:
                    print(f"  Container: <{c['tag']}.{c['className']}> width={c['width']}, maxWidth={c['maxWidth']}")
            except Exception as e:
                print(f"Error {name}: {e}")
                
        await browser.close()

asyncio.run(measure_widths())
