import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 375, 'height': 812})
        page.on('console', lambda msg: print("CONSOLE:", msg.text))
        page.on('pageerror', lambda err: print("PAGE ERROR:", err))
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
        await page.wait_for_timeout(1000)
        
        # Check initial state
        extra_disp = await page.evaluate("() => document.getElementById('bentoExtraGrid') ? getComputedStyle(document.getElementById('bentoExtraGrid')).display : 'none'")
        print("Initial display:", extra_disp)
        
        # Click button
        await page.click('#btnToggleBentoTools')
        await page.wait_for_timeout(500)
        
        after_disp = await page.evaluate("() => document.getElementById('bentoExtraGrid') ? getComputedStyle(document.getElementById('bentoExtraGrid')).display : 'none'")
        btn_text = await page.evaluate("() => document.getElementById('bentoToggleText') ? document.getElementById('bentoToggleText').textContent : ''")
        print("After click 1 display:", after_disp, "btnText:", btn_text)
        
        # Click button again
        await page.click('#btnToggleBentoTools')
        await page.wait_for_timeout(500)
        after_disp2 = await page.evaluate("() => document.getElementById('bentoExtraGrid') ? getComputedStyle(document.getElementById('bentoExtraGrid')).display : 'none'")
        btn_text2 = await page.evaluate("() => document.getElementById('bentoToggleText') ? document.getElementById('bentoToggleText').textContent : ''")
        print("After click 2 display:", after_disp2, "btnText:", btn_text2)
        
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
