import asyncio
from playwright.async_api import async_playwright

async def test_luxury_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        luxury_css = """
        /* Master Luxury Chapter Card Hover */
        .chapter-card {
            transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1), 
                        box-shadow 0.32s cubic-bezier(0.16, 1, 0.3, 1), 
                        border-color 0.32s ease, 
                        background-color 0.32s ease !important;
            will-change: transform, box-shadow !important;
        }
        
        /* Light Mode Normal & Hover */
        html.light .chapter-card {
            background: #ffffff !important;
            border: 1px solid rgba(226, 232, 240, 0.9) !important;
            box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03) !important;
        }
        html.light .chapter-card:hover {
            transform: translateY(-6px) translateZ(0) !important;
            border-color: rgba(16, 185, 129, 0.45) !important;
            box-shadow: 0 20px 38px -10px rgba(15, 23, 42, 0.12), 
                        0 8px 16px -4px rgba(15, 23, 42, 0.05), 
                        0 0 0 1px rgba(16, 185, 129, 0.22) !important;
        }
        
        /* Dark Mode Normal & Hover */
        html.dark .chapter-card {
            background: rgba(18, 24, 38, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        }
        html.dark .chapter-card:hover {
            transform: translateY(-6px) translateZ(0) !important;
            border-color: rgba(52, 211, 153, 0.45) !important;
            box-shadow: 0 24px 44px -10px rgba(0, 0, 0, 0.75), 
                        0 0 26px -4px rgba(16, 185, 129, 0.20), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
        }
        
        /* Orchestrated Child Micro-interactions */
        .chapter-card .btn-action-study {
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .chapter-card:hover .btn-action-study {
            filter: brightness(1.05) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.38) !important;
        }
        
        /* Arrow slides forward smoothly (RTL: left is forward) */
        .chapter-card .btn-arrow-svg {
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
            will-change: transform !important;
        }
        .chapter-card:hover .btn-arrow-svg {
            transform: translateX(-5px) !important;
        }
        
        /* Pill number subtle highlight */
        .chapter-card .ch-pill-num {
            transition: border-color 0.28s ease, background-color 0.28s ease, color 0.28s ease !important;
        }
        .chapter-card:hover .ch-pill-num {
            border-color: rgba(16, 185, 129, 0.4) !important;
            color: var(--text-primary) !important;
        }
        """
        await page.add_style_tag(content=luxury_css)
        await page.wait_for_timeout(400)
        
        card1 = page.locator(".chapter-card").first
        
        # Capture unhovered light
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\luxury_card_normal_light.png")
        
        # Hover light
        await card1.hover()
        await page.wait_for_timeout(400)
        # Capture grid area with card hovered
        grid = page.locator(".chapters-grid")
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\luxury_grid_hover_light.png")
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\luxury_card_hover_light.png")
        
        # Switch to dark mode
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(400)
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\luxury_card_hover_dark.png")
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\luxury_grid_hover_dark.png")
        
        await browser.close()
        print("Luxury hover test completed successfully!")

asyncio.run(test_luxury_hover())
