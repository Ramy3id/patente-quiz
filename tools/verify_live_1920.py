import asyncio
from playwright.async_api import async_playwright

async def verify_live_1920():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        pages = [
            ('Home', 'http://localhost:8080/Capitoli_Divisi/index.html'),
            ('Dashboard', 'http://localhost:8080/interactive_pages/dashboard.html'),
            ('Trucchi', 'http://localhost:8080/interactive_pages/trucchi-esame.html'),
            ('Parole Spia', 'http://localhost:8080/interactive_pages/parole-spia.html'),
            ('Cap 01', 'http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html'),
            ('Incroci', 'http://localhost:8080/interactive_pages/decodificatore-incroci.html'),
            ('Piano Studio', 'http://localhost:8080/interactive_pages/piano-studio.html'),
            ('Scheda Esame', 'http://localhost:8080/interactive_pages/scheda-esame.html')
        ]
        
        print("="*75)
        print("LIVE VERIFICATION ON 1920x1080 (NO INJECTED CSS)")
        print("="*75)
        
        for name, url in pages:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(300)
            
            nav_box = await page.evaluate('''() => {
                const nav = document.querySelector('.unified-portal-nav, #portal-nav, #globalPortalNav');
                return nav ? { x: Math.round(nav.getBoundingClientRect().x), w: Math.round(nav.getBoundingClientRect().width) } : null;
            }''')
            
            banner_box = await page.evaluate('''() => {
                const b = document.querySelector('.guest-free-sample-banner, #guestDashboardNotice, [class*="sample-banner"]');
                return (b && b.offsetParent !== null) ? { x: Math.round(b.getBoundingClientRect().x), w: Math.round(b.getBoundingClientRect().width) } : null;
            }''')
            
            cont_box = await page.evaluate('''() => {
                const c = document.querySelector('.container, .dash-wrapper, .tr-container, .ps-container, .inc-container, .sp-container, .exam-portal-container');
                return c ? { x: Math.round(c.getBoundingClientRect().x), w: Math.round(c.getBoundingClientRect().width) } : null;
            }''')
            
            slug = name.lower().replace(' ', '_')
            await page.screenshot(path=rf'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_live_{slug}.png')
            
            b_str = f"x={banner_box['x']}, w={banner_box['w']}" if banner_box else "NO BANNER"
            c_str = f"x={cont_box['x']}, w={cont_box['w']}" if cont_box else "NO CONT"
            n_str = f"x={nav_box['x']}, w={nav_box['w']}" if nav_box else "NO NAV"
            
            print(f"{name:<15} | NAV: {n_str:<16} | BANNER: {b_str:<18} | CONT: {c_str}")

        await browser.close()
        print("="*75)

asyncio.run(verify_live_1920())
