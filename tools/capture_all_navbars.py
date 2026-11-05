import asyncio
from playwright.async_api import async_playwright

async def capture_all_navbars():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        pages_to_test = [
            ("root_index", "http://localhost:8080/index.html"),
            ("capitoli_index", "http://localhost:8080/Capitoli_Divisi/index.html"),
            ("capitolo_01", "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"),
            ("parole_quiz", "http://localhost:8080/Capitoli_Divisi/parole-quiz.html"),
            ("piano_studio", "http://localhost:8080/interactive_pages/piano-studio.html"),
            ("scheda_esame", "http://localhost:8080/interactive_pages/scheda-esame.html"),
            ("dizionario", "http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html")
        ]
        
        for name, url in pages_to_test:
            try:
                await page.goto(url, wait_until="networkidle", timeout=8000)
                await page.wait_for_timeout(800)
                
                # Check for navbar elements
                nav_info = await page.evaluate("""() => {
                    const nav = document.querySelector('#globalPortalNav') || document.querySelector('nav') || document.querySelector('.navbar') || document.querySelector('header');
                    if (!nav) return { found: false };
                    const cs = window.getComputedStyle(nav);
                    return {
                        found: true,
                        tag: nav.tagName,
                        id: nav.id,
                        className: nav.className,
                        position: cs.position,
                        top: cs.top,
                        hasBefore: !!window.getComputedStyle(nav, '::before').content,
                        beforeContent: window.getComputedStyle(nav, '::before').content,
                        rect: nav.getBoundingClientRect()
                    };
                }""")
                print(f"=== {name} ({url}) ===")
                print(nav_info)
                
                # Take top crop screenshot (top 150px)
                await page.screenshot(
                    path=rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\nav_page_{name}.png",
                    clip={'x': 0, 'y': 0, 'width': 1440, 'height': 150}
                )
            except Exception as e:
                print(f"Error on {name}: {e}")
                
        await browser.close()

asyncio.run(capture_all_navbars())
