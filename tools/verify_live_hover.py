import asyncio
from playwright.async_api import async_playwright
from PIL import Image

async def verify_live_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        # Load local server directly with fresh cache
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        card1 = page.locator(".chapter-card").first
        box = await card1.bounding_box()
        
        # Capture unhovered
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\final_card_normal_light.png")
        
        # Hover
        await card1.hover()
        await page.wait_for_timeout(400)
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\final_card_hover_light.png")
        
        # Check computed styles on hover
        styles = await card1.evaluate("""el => {
            const cs = window.getComputedStyle(el);
            const arrow = el.querySelector('.btn-arrow-svg');
            const arrowCs = window.getComputedStyle(arrow);
            return {
                transform: cs.transform,
                transition: cs.transition,
                boxShadow: cs.boxShadow,
                borderColor: cs.borderColor,
                arrowTransform: arrowCs.transform
            };
        }""")
        print("FINAL VERIFIED HOVER COMPUTED STYLES:")
        for k, v in styles.items():
            print(f"{k}: {v}")
            
        # Capture grid in light
        grid = page.locator(".chapters-grid")
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\final_grid_hover_light.png")
        
        # Switch to dark
        await page.evaluate("document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark');")
        await page.wait_for_timeout(500)
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\final_card_hover_dark.png")
        await grid.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\final_grid_hover_dark.png")
        
        # Generate final GIF
        clip_area = {
            'x': max(0, box['x'] - 15),
            'y': max(0, box['y'] - 15),
            'width': box['width'] + 30,
            'height': box['height'] + 30
        }
        frames = []
        import io
        
        # Back to light mode for the gif
        await page.evaluate("document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light');")
        await page.mouse.move(10, 10)
        await page.wait_for_timeout(400)
        
        # Frame 0
        b0 = await page.screenshot(clip=clip_area)
        frames.append(Image.open(io.BytesIO(b0)))
        
        # Hover
        await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
        for _ in range(8):
            await page.wait_for_timeout(45)
            bf = await page.screenshot(clip=clip_area)
            frames.append(Image.open(io.BytesIO(bf)))
            
        for _ in range(4):
            frames.append(frames[-1])
            
        # Unhover
        await page.mouse.move(10, 10)
        for _ in range(6):
            await page.wait_for_timeout(50)
            bu = await page.screenshot(clip=clip_area)
            frames.append(Image.open(io.BytesIO(bu)))
            
        gif_out = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\final_luxury_hover.gif"
        frames[0].save(gif_out, save_all=True, append_images=frames[1:], duration=60, loop=0)
        print("Final GIF created successfully!")
        
        await browser.close()

asyncio.run(verify_live_hover())
