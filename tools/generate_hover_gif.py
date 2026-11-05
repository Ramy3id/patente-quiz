import asyncio
from playwright.async_api import async_playwright
from PIL import Image

async def capture_hover_frames():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        luxury_css = """
        .chapter-card {
            transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
                        box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
                        border-color 0.35s ease, 
                        background-color 0.35s ease !important;
            will-change: transform, box-shadow !important;
        }
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
        .chapter-card .btn-action-study {
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .chapter-card:hover .btn-action-study {
            filter: brightness(1.05) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.38) !important;
        }
        .chapter-card .btn-arrow-svg {
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
            will-change: transform !important;
        }
        .chapter-card:hover .btn-arrow-svg {
            transform: translateX(-5px) !important;
        }
        """
        await page.add_style_tag(content=luxury_css)
        await page.wait_for_timeout(300)
        
        card1 = page.locator(".chapter-card").first
        box = await card1.bounding_box()
        # Clip area around card with padding
        clip_area = {
            'x': max(0, box['x'] - 15),
            'y': max(0, box['y'] - 15),
            'width': box['width'] + 30,
            'height': box['height'] + 30
        }
        
        frames = []
        
        # Frame 0: unhovered
        img_bytes = await page.screenshot(clip=clip_area)
        import io
        frames.append(Image.open(io.BytesIO(img_bytes)))
        
        # Move mouse over card
        await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
        
        # Capture 8 frames during animation (350ms total)
        for i in range(8):
            await page.wait_for_timeout(45)
            img_bytes = await page.screenshot(clip=clip_area)
            frames.append(Image.open(io.BytesIO(img_bytes)))
            
        # Hold hovered for 4 frames
        for _ in range(4):
            frames.append(frames[-1])
            
        # Move mouse away
        await page.mouse.move(10, 10)
        
        # Capture 6 frames during return
        for i in range(6):
            await page.wait_for_timeout(50)
            img_bytes = await page.screenshot(clip=clip_area)
            frames.append(Image.open(io.BytesIO(img_bytes)))
            
        # Save as animated GIF
        gif_path = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\luxury_hover_motion.gif"
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=60, loop=0)
        print("Generated luxury_hover_motion.gif successfully!")
        
        await browser.close()

asyncio.run(capture_hover_frames())
