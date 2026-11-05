import asyncio
from playwright.async_api import async_playwright

async def test_card_hover_styles():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        # Style 1: The Linear/Stripe Calm Master (Zero jumping, pure diffuse depth, no flash)
        css_style1 = """
        .chapter-card {
            transform: none !important;
            transition: box-shadow 0.25s ease, border-color 0.25s ease !important;
            will-change: auto !important;
        }
        html.light .chapter-card {
            background: #ffffff !important;
            border: 1px solid rgba(15, 23, 42, 0.08) !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 4px 12px rgba(15, 23, 42, 0.02) !important;
        }
        html.light .chapter-card:hover {
            transform: none !important;
            border-color: rgba(15, 23, 42, 0.18) !important;
            box-shadow: 0 14px 30px -4px rgba(15, 23, 42, 0.08), 0 4px 10px -2px rgba(15, 23, 42, 0.03) !important;
        }
        html.dark .chapter-card {
            background: rgba(18, 24, 38, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
        }
        html.dark .chapter-card:hover {
            transform: none !important;
            border-color: rgba(255, 255, 255, 0.18) !important;
            box-shadow: 0 14px 32px -4px rgba(0, 0, 0, 0.7) !important;
        }
        /* Button subtle response */
        .chapter-card .btn-action-study {
            transition: filter 0.2s ease, box-shadow 0.2s ease !important;
            transform: none !important;
        }
        .chapter-card:hover .btn-action-study {
            filter: brightness(1.05) !important;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35) !important;
        }
        .chapter-card .btn-arrow-svg {
            transition: transform 0.2s ease !important;
        }
        .chapter-card:hover .btn-arrow-svg {
            transform: translateX(-3px) !important;
        }
        /* No other elements moving */
        .chapter-card .ch-pill-num, .chapter-card .stat-pill {
            transform: none !important;
        }
        """
        await page.add_style_tag(content=css_style1)
        await page.wait_for_timeout(300)
        
        card1 = page.locator(".chapter-card").first
        await card1.hover()
        await page.wait_for_timeout(300)
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\style1_linear_hover.png")
        
        # Style 2: The Ultra-Soft Micro-Lift (Only -2px, soft ease-out, no bouncing)
        css_style2 = """
        .chapter-card {
            transition: transform 0.22s ease-out, box-shadow 0.22s ease-out, border-color 0.22s ease !important;
        }
        html.light .chapter-card:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(15, 23, 42, 0.16) !important;
            box-shadow: 0 12px 28px -4px rgba(15, 23, 42, 0.08) !important;
        }
        html.dark .chapter-card:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(255, 255, 255, 0.16) !important;
            box-shadow: 0 16px 32px -4px rgba(0, 0, 0, 0.65) !important;
        }
        """
        await page.add_style_tag(content=css_style2)
        await page.wait_for_timeout(300)
        await card1.hover()
        await page.wait_for_timeout(300)
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\style2_microlift_hover.png")
        
        await browser.close()
        print("Styles tested!")

asyncio.run(test_card_hover_styles())
