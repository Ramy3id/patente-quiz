import asyncio
from playwright.async_api import async_playwright

async def render_final_curved_top():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        css = """
        #globalPortalNav::before {
            content: '' !important;
            position: absolute !important;
            inset: 0 !important;
            border-radius: 18px !important;
            padding: 2.5px !important;
            background: linear-gradient(to right, 
              #009246 0%, #009246 33.33%, 
              #ffffff 33.33%, #ffffff 66.66%, 
              #ce2b37 66.66%, #ce2b37 100%
            ) !important;
            -webkit-mask: 
               linear-gradient(#fff 0 0) content-box, 
               linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
                    mask-composite: exclude;
            pointer-events: none !important;
            z-index: 10 !important;
            clip-path: polygon(0 0, 100% 0, 100% 22px, 0 22px) !important;
            box-shadow: 0 2px 10px rgba(206, 43, 55, 0.12) !important;
        }
        html.light #globalPortalNav::before {
            background: linear-gradient(to right, 
              #009246 0%, #009246 33.33%, 
              #ffffff 33.33%, #ffffff 66.66%, 
              #ce2b37 66.66%, #ce2b37 100%
            ) !important;
            box-shadow: 0 2px 10px rgba(206, 43, 55, 0.08) !important;
        }
        """
        await page.add_style_tag(content=css)
        await page.wait_for_timeout(400)
        
        nav = page.locator("#globalPortalNav")
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\top_arch_nav_light.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\top_arch_full_light.png")
        
        # Open Megamenu to show how clean it looks below the nav!
        chapters_btn = page.locator("#navChaptersBtn")
        if await chapters_btn.count() > 0:
            await chapters_btn.click()
            await page.wait_for_timeout(500)
            await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\top_arch_megamenu_open.png")
            # Close it
            await page.mouse.click(10, 10)
            await page.wait_for_timeout(300)
            
        # Switch to dark mode
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(500)
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\top_arch_nav_dark.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\top_arch_full_dark.png")
        
        await browser.close()

asyncio.run(render_final_curved_top())
