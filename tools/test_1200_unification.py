import asyncio
from playwright.async_api import async_playwright

async def test_1200_unification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        test_rule = """
        .container,
        main.container,
        div.container,
        .ch-portal-container,
        .sp-container,
        .inc-container,
        .exam-portal-container,
        .dict-container,
        .interactive-container,
        .quiz-container,
        .content-wrapper {
          max-width: 1200px !important;
          width: 100% !important;
          margin-left: auto !important;
          margin-right: auto !important;
          box-sizing: border-box !important;
        }
        """
        
        pages = [
            ("capitoli_home", "http://localhost:8080/Capitoli_Divisi/index.html"),
            ("capitolo_01", "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"),
            ("capitolo_13", "http://localhost:8080/Capitoli_Divisi/Capitolo_13_norme_di_circolazione/index.html"),
            ("dizionario", "http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html"),
            ("parole_quiz", "http://localhost:8080/Capitoli_Divisi/parole-quiz.html"),
            ("piano_studio", "http://localhost:8080/interactive_pages/piano-studio.html"),
            ("scheda_esame", "http://localhost:8080/interactive_pages/scheda-esame.html"),
            ("decodificatore", "http://localhost:8080/interactive_pages/decodificatore-incroci.html")
        ]
        
        for name, url in pages:
            await page.goto(url, wait_until="networkidle")
            await page.add_style_tag(content=test_rule)
            await page.wait_for_timeout(400)
            
            # Check main container width
            w = await page.evaluate("""() => {
                const el = document.querySelector('.container, .sp-container, .inc-container, .exam-portal-container, .ch-portal-container');
                return el ? el.getBoundingClientRect().width : 0;
            }""")
            print(f"{name}: container width = {w}px")
            
            # Capture full desktop screenshot
            await page.screenshot(path=rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\unified1200_{name}.png")
            
        await browser.close()

asyncio.run(test_1200_unification())
