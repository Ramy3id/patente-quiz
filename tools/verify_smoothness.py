import asyncio
from playwright.async_api import async_playwright

async def verify_smoothness():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        master_hover_css = """
        /* ==========================================================================
           MASTER LUXURY CHAPTER CARD HOVER SYSTEM (Apple / Stripe Fluid Physics)
           ========================================================================== */
        .chapter-card {
            transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
                        box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
                        border-color 0.35s ease, 
                        background 0.35s ease !important;
            will-change: transform, box-shadow !important;
            transform: translateZ(0) !important;
            backface-visibility: hidden !important;
        }

        /* Light Mode Normal */
        html.light .chapter-card {
            background: #ffffff !important;
            border: 1px solid rgba(226, 232, 240, 0.95) !important;
            box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05), 0 1px 3px rgba(15, 23, 42, 0.03) !important;
        }

        /* Light Mode Hover */
        html.light .chapter-card:hover {
            transform: translateY(-6px) translateZ(0) !important;
            border-color: rgba(16, 185, 129, 0.45) !important;
            box-shadow: 0 22px 40px -10px rgba(15, 23, 42, 0.12), 
                        0 8px 18px -4px rgba(15, 23, 42, 0.04), 
                        0 0 0 1px rgba(16, 185, 129, 0.22) !important;
        }

        /* Dark Mode Normal */
        html.dark .chapter-card {
            background: rgba(18, 24, 38, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        }

        /* Dark Mode Hover */
        html.dark .chapter-card:hover {
            transform: translateY(-6px) translateZ(0) !important;
            border-color: rgba(52, 211, 153, 0.45) !important;
            box-shadow: 0 24px 48px -10px rgba(0, 0, 0, 0.75), 
                        0 0 26px -4px rgba(16, 185, 129, 0.22), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
        }

        /* Active / Pressed state */
        .chapter-card:active {
            transform: translateY(-2px) scale(0.992) !important;
            transition: transform 0.1s ease !important;
        }

        /* Micro-interactions: Start Study Button */
        .chapter-card .btn-action-study {
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                        box-shadow 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                        filter 0.28s ease !important;
        }
        .chapter-card:hover .btn-action-study {
            filter: brightness(1.06) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.42) !important;
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
            background: rgba(16, 185, 129, 0.08) !important;
        }

        /* Stat pills subtle response */
        .chapter-card .stat-pill {
            transition: border-color 0.28s ease !important;
        }
        .chapter-card:hover .stat-pill {
            border-color: rgba(16, 185, 129, 0.22) !important;
        }
        """
        await page.add_style_tag(content=master_hover_css)
        await page.wait_for_timeout(400)
        
        # Test hover on card 2 (Capitolo 02)
        card2 = page.locator(".chapter-card").nth(1)
        await card2.hover()
        await page.wait_for_timeout(400)
        
        grid = page.locator(".chapters-grid")
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_grid_hover_light.png")
        await card2.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_card2_hover_light.png")
        
        # Switch to dark
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(400)
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_grid_hover_dark.png")
        await card2.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_card2_hover_dark.png")
        
        await browser.close()
        print("Verified smoothness captured successfully!")

asyncio.run(verify_smoothness())
