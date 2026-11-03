import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 375, "height": 812})
        await page.goto("http://localhost:8080/interactive_pages/dashboard.html")
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        
        tabs = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.dash-tab-btn'));
            return btns.map(b => ({
                text: b.innerText.trim(),
                box: b.getBoundingClientRect()
            }));
        }""")
        for t in tabs:
            print(t["text"], t["box"])
            
        overlap = await page.evaluate("""() => {
            const bar = document.querySelector('.dash-tabs-bar');
            const nextEl = bar ? bar.nextElementSibling : null;
            return {
                barBox: bar ? bar.getBoundingClientRect() : null,
                nextBox: nextEl ? nextEl.getBoundingClientRect() : null,
                nextTag: nextEl ? (nextEl.tagName + '.' + nextEl.className) : null
            };
        }""")
        print("Overlap:", overlap)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect())
