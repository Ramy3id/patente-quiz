import asyncio
from playwright.async_api import async_playwright

async def verify_final():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        # Load local server with fresh cache
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        nav = page.locator("#globalPortalNav")
        box = await nav.bounding_box()
        
        # 1. Nav in light mode
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\nav_top_arch_final_light.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\full_page_top_arch_light.png")
        
        # 2. Closeup corners
        # Green Left Corner
        await page.screenshot(
            path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\corner_left_green_final.png",
            clip={'x': box['x'] - 5, 'y': box['y'] - 5, 'width': 85, 'height': 55}
        )
        # Red Right Corner
        await page.screenshot(
            path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\corner_right_red_final.png",
            clip={'x': box['x'] + box['width'] - 80, 'y': box['y'] - 5, 'width': 85, 'height': 55}
        )
        
        # 3. Megamenu open test
        chapters_btn = page.locator("#navChaptersBtn")
        if await chapters_btn.count() > 0:
            await chapters_btn.click()
            await page.wait_for_timeout(500)
            await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\megamenu_open_final.png")
            await page.mouse.click(10, 10)
            await page.wait_for_timeout(300)
            
        # 4. Dark mode
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(600)
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\nav_top_arch_final_dark.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\full_page_top_arch_dark.png")
        
        await browser.close()
        print("All final verification screenshots captured!")

asyncio.run(verify_final())
