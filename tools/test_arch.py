import asyncio
from playwright.async_api import async_playwright

async def test_top_curved_arch():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        # Test 1: Sharp cutoff right after corner (e.g. 22px)
        css_arch_sharp = """
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
        """
        
        # Test 2: Smooth fade out on the sides
        # Using mask with vertical fade
        # In CSS, can combine masks or use clip-path + linear-gradient mask
        css_arch_fade = """
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
               linear-gradient(to bottom, #000 0px, #000 16px, rgba(0,0,0,0.5) 22px, transparent 28px),
               linear-gradient(#fff 0 0) content-box;
            -webkit-mask-composite: destination-in, xor;
            pointer-events: none !important;
            z-index: 10 !important;
        }
        """
        
        # Let's test with clip-path values: 18px (just the corner), 24px (turns corner and drops a bit), 30px
        for h_cut in [18, 22, 26]:
            test_css = f"""
            #globalPortalNav::before {{
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
                clip-path: polygon(0 0, 100% 0, 100% {h_cut}px, 0 {h_cut}px) !important;
            }}
            """
            await page.add_style_tag(content=test_css)
            await page.wait_for_timeout(300)
            nav = page.locator("#globalPortalNav")
            await nav.screenshot(path=rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\arch_cut_{h_cut}_light.png")
            
            # Closeups of the corners
            box = await nav.bounding_box()
            # Left corner (green)
            await page.screenshot(
                path=rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\arch_cut_{h_cut}_left_green.png",
                clip={'x': box['x'] - 5, 'y': box['y'] - 5, 'width': 80, 'height': 50}
            )
            # Right corner (red)
            await page.screenshot(
                path=rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\arch_cut_{h_cut}_right_red.png",
                clip={'x': box['x'] + box['width'] - 75, 'y': box['y'] - 5, 'width': 80, 'height': 50}
            )

        await browser.close()

asyncio.run(test_top_curved_arch())
