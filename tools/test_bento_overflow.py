import asyncio
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 375, 'height': 812})
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
        await page.wait_for_timeout(1000)
        
        res = await page.evaluate('''() => {
            const docW = document.documentElement.clientWidth;
            const docSw = document.documentElement.scrollWidth;
            const bodySw = document.body.scrollWidth;
            
            const cards = [];
            document.querySelectorAll('.bento-card').forEach((c, i) => {
                const r = c.getBoundingClientRect();
                const title = c.querySelector('.bento-title') ? c.querySelector('.bento-title').innerText : '';
                cards.push({
                    i: i + 1,
                    title: title,
                    left: Math.round(r.left),
                    right: Math.round(r.right),
                    width: Math.round(r.width),
                    overflowsLeft: r.left < 0,
                    overflowsRight: r.right > docW
                });
            });
            
            return {
                docW,
                docSw,
                bodySw,
                cards
            };
        }''')
        
        print(f"Viewport docW: {res['docW']}px | docSw: {res['docSw']}px | bodySw: {res['bodySw']}px")
        print("=== BENTO CARDS POSITION AUDIT ===")
        all_ok = True
        for c in res['cards']:
            status = "🔴 OVERFLOW" if c['overflowsLeft'] or c['overflowsRight'] else "🟢 OK"
            if c['overflowsLeft'] or c['overflowsRight']: all_ok = False
            print(f"{status} #{c['i']} '{c['title']}' -> left: {c['left']}px, right: {c['right']}px, width: {c['width']}px")
            
        print(f"\nOVERALL RESULT: {'✅ PERFECT (NO OVERFLOW)' if all_ok and res['bodySw'] <= 375 and res['docSw'] <= 375 else '❌ STILL HAS OVERFLOW'}")
        
        # Take verification screenshot
        bento_sec = await page.query_selector('.bento-tools-section')
        if bento_sec:
            await bento_sec.screenshot(path='C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_bento_zero_overflow.png')
            print("Saved screenshot to verified_bento_zero_overflow.png")
            
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
