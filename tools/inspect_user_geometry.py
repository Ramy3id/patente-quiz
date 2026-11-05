import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use full HD desktop 1920x1080 (matching user's screen)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        pages = [
            ('home', 'http://localhost:8080/Capitoli_Divisi/index.html'),
            ('dashboard', 'http://localhost:8080/interactive_pages/dashboard.html'),
            ('trucchi', 'http://localhost:8080/interactive_pages/trucchi-esame.html'),
            ('parole_spia', 'http://localhost:8080/interactive_pages/parole-spia.html'),
            ('cap01', 'http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html'),
            ('incroci', 'http://localhost:8080/interactive_pages/decodificatore-incroci.html')
        ]
        
        for name, url in pages:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(300)
            
            # Check nav rect
            nav_box = await page.evaluate('''() => {
                const nav = document.querySelector('.unified-portal-nav, #portal-nav, #globalPortalNav');
                return nav ? { x: nav.getBoundingClientRect().x, w: nav.getBoundingClientRect().width } : null;
            }''')
            
            # Check banner rect
            banner_box = await page.evaluate('''() => {
                const b = document.querySelector('.guest-free-sample-banner, #guestDashboardNotice, [class*="sample-banner"], [id*="guest"]');
                return b ? { x: b.getBoundingClientRect().x, w: b.getBoundingClientRect().width } : null;
            }''')
            
            # Check main container rect
            cont_box = await page.evaluate('''() => {
                const c = document.querySelector('.container, .dash-wrapper, .tr-container, .ps-container, .inc-container, .sp-container, .exam-portal-container');
                return c ? { x: c.getBoundingClientRect().x, w: c.getBoundingClientRect().width } : null;
            }''')
            
            print(f'=== {name.upper()} ===')
            print('NAV:    ', f'x={nav_box["x"]:.1f}, w={nav_box["w"]:.1f}' if nav_box else 'NONE')
            print('BANNER: ', f'x={banner_box["x"]:.1f}, w={banner_box["w"]:.1f}' if banner_box else 'NONE')
            print('CONT:   ', f'x={cont_box["x"]:.1f}, w={cont_box["w"]:.1f}' if cont_box else 'NONE')
            
            # Take screenshot to examine
            await page.screenshot(path=rf'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/user_view_{name}.png')
            
        await browser.close()

asyncio.run(inspect())
