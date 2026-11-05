import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import io

async def verify_option1():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        card1 = page.locator(".chapter-card").first
        
        # Check computed styles on normal
        cs_norm = await card1.evaluate("el => window.getComputedStyle(el).transform")
        print("NORMAL TRANSFORM:", cs_norm)
        
        # Hover
        await card1.hover()
        await page.wait_for_timeout(300)
        cs_hover = await card1.evaluate("el => ({ transform: window.getComputedStyle(el).transform, boxShadow: window.getComputedStyle(el).boxShadow, borderColor: window.getComputedStyle(el).borderColor })")
        print("HOVER COMPUTED:", cs_hover)
        
        # Capture grid
        grid = page.locator(".chapters-grid")
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\option1_grid_light.png")
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\option1_card_light.png")
        
        # Dark mode
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(500)
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\option1_grid_dark.png")
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\option1_card_dark.png")
        
        # Switch back to light to record sweeping mouse across 3 cards
        await page.evaluate("document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light');")
        await page.wait_for_timeout(400)
        
        # Record rapid mouse sweep across cards row 1 to prove stability
        cards = page.locator(".chapter-card")
        c1_box = await cards.nth(0).bounding_box()
        c2_box = await cards.nth(1).bounding_box()
        c3_box = await cards.nth(2).bounding_box()
        
        row_area = {
            'x': max(0, c3_box['x'] - 10),
            'y': max(0, c1_box['y'] - 10),
            'width': (c1_box['x'] + c1_box['width']) - c3_box['x'] + 20,
            'height': c1_box['height'] + 20
        }
        
        frames = []
        # Sweep from card 3 to card 2 to card 1
        points = [
            (c3_box['x'] + 100, c3_box['y'] + 100),
            (c2_box['x'] + 100, c2_box['y'] + 100),
            (c1_box['x'] + 100, c1_box['y'] + 100),
            (10, 10)
        ]
        
        for pt in points:
            await page.mouse.move(pt[0], pt[1])
            for _ in range(3):
                await page.wait_for_timeout(60)
                b = await page.screenshot(clip=row_area)
                frames.append(Image.open(io.BytesIO(b)))
                
        gif_path = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\option1_sweep_stable.gif"
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=70, loop=0)
        print("Saved option1_sweep_stable.gif")
        
        await browser.close()

asyncio.run(verify_option1())
