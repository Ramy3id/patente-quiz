import asyncio
from playwright.async_api import async_playwright

async def inspect_nav_dom():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        # 1. Capitoli index
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(500)
        dom1 = await page.evaluate("() => document.getElementById('globalPortalNav').outerHTML")
        
        # 2. Capitolo 01
        await page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html", wait_until="networkidle")
        await page.wait_for_timeout(500)
        dom2 = await page.evaluate("() => document.getElementById('globalPortalNav').outerHTML")
        
        # 3. Piano Studio
        await page.goto("http://localhost:8080/interactive_pages/piano-studio.html", wait_until="networkidle")
        await page.wait_for_timeout(500)
        dom3 = await page.evaluate("() => document.getElementById('globalPortalNav').outerHTML")
        
        print("DOM 1 length:", len(dom1))
        print("DOM 2 length:", len(dom2))
        print("DOM 3 length:", len(dom3))
        
        import difflib
        diff = difflib.unified_diff(dom1.splitlines(), dom2.splitlines(), lineterm='')
        print("\n--- DIFF BETWEEN capitoli_index AND capitolo_01 ---")
        for line in list(diff)[:30]:
            print(line.encode('ascii', 'backslashreplace').decode('ascii'))
            
        await browser.close()

asyncio.run(inspect_nav_dom())
