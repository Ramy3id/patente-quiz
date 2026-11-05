import asyncio
from playwright.async_api import async_playwright

async def verify_universal_nav():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        pages = [
            ("capitoli_home", "http://localhost:8080/Capitoli_Divisi/index.html"),
            ("capitolo_01", "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"),
            ("capitolo_13", "http://localhost:8080/Capitoli_Divisi/Capitolo_13_norme_di_circolazione/index.html"),
            ("dizionario", "http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html"),
            ("piano_studio", "http://localhost:8080/interactive_pages/piano-studio.html"),
            ("scheda_esame", "http://localhost:8080/interactive_pages/scheda-esame.html")
        ]
        
        for name, url in pages:
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(600)
            
            nav = page.locator("#globalPortalNav, .unified-portal-nav").first
            await nav.screenshot(path=rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\universal_{name}.png")
            print(f"Captured universal_{name}.png")
            
        await browser.close()

asyncio.run(verify_universal_nav())
