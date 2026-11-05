import asyncio
from playwright.async_api import async_playwright

async def generate_comparisons():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        # 1. Option Top Accent (only top border with curved top corners)
        # We can apply CSS: border-top + border-radius on top, or mask
        css_top = """
        #globalPortalNav::before {
            display: none !important;
        }
        #globalPortalNav::after {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            height: 3px !important;
            border-top-left-radius: 18px !important;
            border-top-right-radius: 18px !important;
            background: linear-gradient(to right, #009246 0%, #009246 33.33%, #ffffff 33.33%, #ffffff 66.66%, #ce2b37 66.66%, #ce2b37 100%) !important;
            box-shadow: 0 1px 6px rgba(206, 43, 55, 0.15) !important;
            pointer-events: none !important;
            z-index: 10 !important;
        }
        """
        await page.add_style_tag(content=css_top)
        await page.wait_for_timeout(400)
        nav = page.locator("#globalPortalNav")
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_top_light.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_top_full_light.png")
        
        # Dark mode top
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(400)
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_top_dark.png")
        
        # 2. Option Bottom Accent (only bottom border with curved bottom corners)
        # Reload page fresh
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(600)
        css_bottom = """
        #globalPortalNav::before {
            display: none !important;
        }
        #globalPortalNav::after {
            content: '' !important;
            position: absolute !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            height: 3px !important;
            border-bottom-left-radius: 18px !important;
            border-bottom-right-radius: 18px !important;
            background: linear-gradient(to right, #009246 0%, #009246 33.33%, #ffffff 33.33%, #ffffff 66.66%, #ce2b37 66.66%, #ce2b37 100%) !important;
            box-shadow: 0 -1px 6px rgba(206, 43, 55, 0.15) !important;
            pointer-events: none !important;
            z-index: 10 !important;
        }
        """
        await page.add_style_tag(content=css_bottom)
        await page.wait_for_timeout(400)
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_bottom_light.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_bottom_full_light.png")
        
        # Dark mode bottom
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(400)
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_bottom_dark.png")
        
        await browser.close()

asyncio.run(generate_comparisons())
