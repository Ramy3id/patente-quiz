import asyncio
from playwright.async_api import async_playwright

async def inspect_hover_now():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        
        card1 = page.locator(".chapter-card").first
        
        # Capture unhovered
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\card_normal_current.png")
        
        # Hover
        await card1.hover()
        await page.wait_for_timeout(300)
        await card1.screenshot(path=r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\card_hover_current.png")
        
        # Check computed styles on hover
        styles = await card1.evaluate("""el => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                transition: cs.transition,
                boxShadow: cs.boxShadow,
                borderColor: cs.borderColor
            };
        }""")
        print("CURRENT HOVER COMPUTED STYLES:")
        for k, v in styles.items():
            print(f"{k}: {v}")
            
        await browser.close()

asyncio.run(inspect_hover_now())
