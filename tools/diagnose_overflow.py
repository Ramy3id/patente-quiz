import asyncio
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 375, 'height': 812})
        await page.goto('http://localhost:8080/interactive_pages/scheda-esame.html')
        await page.wait_for_timeout(1000)
        res = await page.evaluate('''() => {
            const docW = document.documentElement.clientWidth;
            const res = [];
            const doc = document.documentElement;
            res.push({
                docScrollWidth: doc.scrollWidth,
                docClientWidth: doc.clientWidth,
                bodyScrollWidth: document.body ? document.body.scrollWidth : 0,
                bodyClientWidth: document.body ? document.body.clientWidth : 0
            });
            
            document.querySelectorAll('*').forEach(el => {
                const r = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                if (r.right > docW + 1) {
                    res.push({
                        TYPE: 'RIGHT_OVERFLOW',
                        tag: el.tagName,
                        id: el.id,
                        cls: el.className,
                        right: r.right,
                        width: r.width,
                        overflowX: style.overflowX
                    });
                }
                if (r.left < -1) {
                    // Check if parent has overflow-x auto/hidden
                    let p = el.parentElement;
                    let hasHiddenParent = false;
                    while (p) {
                        const ps = window.getComputedStyle(p);
                        if (ps.overflowX === 'hidden' || ps.overflowX === 'auto' || ps.overflowX === 'scroll') {
                            hasHiddenParent = true;
                            break;
                        }
                        p = p.parentElement;
                    }
                    if (!hasHiddenParent) {
                        res.push({
                            TYPE: 'UNCONTAINED_LEFT_OVERFLOW',
                            tag: el.tagName,
                            id: el.id,
                            cls: el.className,
                            left: r.left,
                            width: r.width
                        });
                    }
                }
            });
            return res;
        }''')
        for x in res:
            print(x)
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
