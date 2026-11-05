import asyncio
from playwright.async_api import async_playwright

async def test_perfect_alignment():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        test_css = """
        /* Master Container Unification */
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
        .content-wrapper,
        .study-plan-container,
        .lab-container,
        .zero-mistake-container,
        .dash-wrapper,
        .tr-container,
        .ps-container,
        .cq-container,
        .zm-container,
        .privacy-container {
          max-width: 1200px !important;
          width: 100% !important;
          padding-left: 18px !important;
          padding-right: 18px !important;
          margin-left: auto !important;
          margin-right: auto !important;
          box-sizing: border-box !important;
        }

        /* Master Banner Unification */
        .guest-free-sample-banner,
        #guestIncrociBanner,
        #guestParoleBanner,
        #guestTrucchiBanner,
        #guestPianoBanner,
        #guestDashboardNotice,
        [class*="sample-banner"] {
          max-width: 1164px !important;
          width: calc(100% - 36px) !important;
          margin: 16px auto !important;
          box-sizing: border-box !important;
        }
        """
        
        pages = [
            ('Home', 'http://localhost:8080/Capitoli_Divisi/index.html'),
            ('Dashboard', 'http://localhost:8080/interactive_pages/dashboard.html'),
            ('Trucchi', 'http://localhost:8080/interactive_pages/trucchi-esame.html'),
            ('Parole Spia', 'http://localhost:8080/interactive_pages/parole-spia.html'),
            ('Cap 01', 'http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html'),
            ('Incroci', 'http://localhost:8080/interactive_pages/decodificatore-incroci.html')
        ]
        
        for name, url in pages:
            await page.goto(url, wait_until='networkidle')
            await page.add_style_tag(content=test_css)
            await page.wait_for_timeout(200)
            
            nav_box = await page.evaluate('''() => {
                const nav = document.querySelector('.unified-portal-nav, #portal-nav, #globalPortalNav');
                return nav ? { x: nav.getBoundingClientRect().x, w: nav.getBoundingClientRect().width } : null;
            }''')
            
            banner_box = await page.evaluate('''() => {
                const b = document.querySelector('.guest-free-sample-banner, #guestDashboardNotice, [class*="sample-banner"], [id*="guest"]');
                return b ? { x: b.getBoundingClientRect().x, w: b.getBoundingClientRect().width } : null;
            }''')
            
            cont_box = await page.evaluate('''() => {
                const c = document.querySelector('.container, .dash-wrapper, .tr-container, .ps-container, .inc-container, .sp-container, .exam-portal-container');
                return c ? { x: c.getBoundingClientRect().x, w: c.getBoundingClientRect().width } : null;
            }''')
            
            print(f'=== {name.upper()} ===')
            print('NAV:    ', f'x={nav_box["x"]:.1f}, w={nav_box["w"]:.1f}' if nav_box else 'NONE')
            print('BANNER: ', f'x={banner_box["x"]:.1f}, w={banner_box["w"]:.1f}' if banner_box else 'NONE')
            print('CONT:   ', f'x={cont_box["x"]:.1f}, w={cont_box["w"]:.1f}' if cont_box else 'NONE')
            
            # Screenshot
            slug = name.lower().replace(' ', '_')
            await page.screenshot(path=rf'C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/fixed_grid_{slug}.png')
            
        await browser.close()

asyncio.run(test_perfect_alignment())
