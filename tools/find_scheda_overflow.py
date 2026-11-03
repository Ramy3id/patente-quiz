import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 375, 'height': 812})
        await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html')
        await page.wait_for_timeout(1000)
        res = await page.evaluate('''() => {
            const bad = [];
            document.querySelectorAll('*').forEach(el => {
                // If element has offsetWidth > 375 or scrollWidth > 375 when it should fit
                if (el.scrollWidth > 375 && !['HTML', 'BODY'].includes(el.tagName)) {
                    const style = window.getComputedStyle(el);
                    bad.push({
                        tag: el.tagName,
                        id: el.id,
                        cls: el.className,
                        scrollWidth: el.scrollWidth,
                        clientWidth: el.clientWidth,
                        offsetWidth: el.offsetWidth,
                        overflowX: style.overflowX
                    });
                }
            });
            return bad;
        }''')
        for x in res:
            print(x)
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
