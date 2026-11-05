import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        # Load local server
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Capture current light mode nav
        nav = page.locator("#globalPortalNav")
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\current_nav_light.png")
        
        # Switch to dark mode
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(500)
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\current_nav_dark.png")
        
        await browser.close()

asyncio.run(run())
