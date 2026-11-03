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
        
        # Check initial
        initial = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.subtopic-chip'));
            return btns.map(b => ({
                text: b.innerText.trim(),
                h: b.getBoundingClientRect().height,
                w: b.getBoundingClientRect().width
            })).filter(x => x.h > 0);
        }""")
        print(f"Initial visible chips count: {len(initial)}")
        for x in initial:
            print("-", x["text"], x["w"], x["h"])
            
        # Click toggle
        await page.click("#btnToggleExtraSubtopics")
        await page.wait_for_timeout(200)
        
        expanded = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.subtopic-chip'));
            const txt = document.getElementById('extraSubtopicsToggleText');
            return {
                toggleText: txt ? txt.innerText : null,
                visible: btns.map(b => ({
                    text: b.innerText.trim(),
                    h: b.getBoundingClientRect().height,
                    w: b.getBoundingClientRect().width
                })).filter(x => x.h > 0)
            };
        }""")
        print(f"Expanded toggle text: {expanded['toggleText']}")
        print(f"Expanded visible chips count: {len(expanded['visible'])}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect())
