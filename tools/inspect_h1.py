import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 375, "height": 812})
        await page.goto("http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html")
        
        h1_info = await page.evaluate("""() => {
            const h1 = document.querySelector('.hero-main-card h1');
            const spans = h1 ? Array.from(h1.querySelectorAll('span')).map(s => ({ text: s.innerText, box: s.getBoundingClientRect() })) : [];
            return {
                h1_dir: h1 ? window.getComputedStyle(h1).direction : null,
                h1_display: h1 ? window.getComputedStyle(h1).display : null,
                h1_box: h1 ? h1.getBoundingClientRect() : null,
                spans: spans
            };
        }""")
        print("H1 info:", h1_info)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect())
