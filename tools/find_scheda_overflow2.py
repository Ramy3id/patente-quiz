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
            const docW = document.documentElement.clientWidth;
            document.querySelectorAll('*').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.right > docW + 1) {
                    bad.push({tag: el.tagName, id: el.id, cls: el.className, right: r.right, left: r.left, width: r.width});
                }
            });
            return {
                docScrollWidth: document.documentElement.scrollWidth,
                badCount: bad.length,
                bad: bad
            };
        }''')
        print(f"docScrollWidth: {res['docScrollWidth']}, badCount: {res['badCount']}")
        for x in res['bad']:
            print(x)
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
