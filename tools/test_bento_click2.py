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
        
        info = await page.evaluate('''() => {
            const btn = document.getElementById('btnToggleBentoTools');
            const extra = document.getElementById('bentoExtraGrid');
            return {
                btnExists: !!btn,
                extraExists: !!extra,
                btnText: btn ? btn.innerText : null,
                extraDisplay: extra ? getComputedStyle(extra).display : null,
                extraInlineDisplay: extra ? extra.style.display : null,
                allCardsCount: document.querySelectorAll('.bento-card').length,
                visibleCardsCount: Array.from(document.querySelectorAll('.bento-card')).filter(c => c.offsetHeight > 0).length
            };
        }''')
        print("BENTO STATE:", info)
        
        # Test click
        await page.click('#btnToggleBentoTools')
        await page.wait_for_timeout(500)
        
        info_after = await page.evaluate('''() => {
            const btn = document.getElementById('btnToggleBentoTools');
            const extra = document.getElementById('bentoExtraGrid');
            return {
                btnText: btn ? btn.innerText : null,
                extraDisplay: extra ? getComputedStyle(extra).display : null,
                visibleCardsCount: Array.from(document.querySelectorAll('.bento-card')).filter(c => c.offsetHeight > 0).length
            };
        }''')
        print("AFTER CLICK:", info_after)
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
