import asyncio
from playwright.async_api import async_playwright
from PIL import Image

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        # Load local page
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        nav = page.locator("#globalPortalNav")
        
        # Light mode
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_nav_light.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_full_light.png")
        
        # Dark mode
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(600)
        await nav.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_nav_dark.png")
        await page.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_full_dark.png")
        
        await browser.close()

asyncio.run(verify())

# Sample pixels
im_light = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_nav_light.png")
w, h = im_light.size
print("LIGHT MODE PIXELS at y=1:")
print("x=10% (Green):", im_light.getpixel((int(w * 0.1), 1)))
print("x=50% (White):", im_light.getpixel((int(w * 0.5), 1)))
print("x=90% (Red):  ", im_light.getpixel((int(w * 0.9), 1)))

im_dark = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_nav_dark.png")
print("\nDARK MODE PIXELS at y=1:")
print("x=10% (Green):", im_dark.getpixel((int(w * 0.1), 1)))
print("x=50% (White):", im_dark.getpixel((int(w * 0.5), 1)))
print("x=90% (Red):  ", im_dark.getpixel((int(w * 0.9), 1)))
