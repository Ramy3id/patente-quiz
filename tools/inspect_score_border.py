import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 375, "height": 812})
        url = "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"
        await page.goto(url, wait_until="networkidle")
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        
        info = await page.evaluate("""() => {
            const strip = document.querySelector('.score-strip');
            const parent = strip ? strip.parentElement : null;
            const csStrip = strip ? window.getComputedStyle(strip) : null;
            const csParent = parent ? window.getComputedStyle(parent) : null;
            return {
                strip_border: csStrip ? csStrip.border : null,
                strip_border_top: csStrip ? csStrip.borderTop : null,
                strip_border_left: csStrip ? csStrip.borderLeft : null,
                strip_border_right: csStrip ? csStrip.borderRight : null,
                strip_border_bottom: csStrip ? csStrip.borderBottom : null,
                strip_border_radius: csStrip ? csStrip.borderRadius : null,
                strip_bg: csStrip ? csStrip.backgroundColor : null,
                parent_tag: parent ? (parent.tagName + '.' + parent.className) : null,
                parent_border: csParent ? csParent.border : null
            };
        }""")
        print("Score strip computed styles:", info)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect())
