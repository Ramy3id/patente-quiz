import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 375, 'height': 812})
        await page.goto('http://localhost:8080/interactive_pages/parole-spia.html')
        await page.wait_for_timeout(1000)
        res = await page.evaluate('''() => {
            const nav = document.getElementById('globalPortalNav');
            if (!nav) return 'no nav';
            const matched = [];
            // Check all stylesheets
            for (let sheet of document.styleSheets) {
                try {
                    for (let rule of sheet.cssRules) {
                        if (rule.selectorText && (rule.selectorText.includes('unified-portal-nav') || rule.selectorText.includes('globalPortalNav') || rule.selectorText.includes('#portal-nav'))) {
                            matched.push({
                                href: sheet.href ? sheet.href.split('/').pop() : 'inline',
                                selector: rule.selectorText,
                                cssText: rule.cssText
                            });
                        }
                    }
                } catch(e) {}
            }
            return {
                matched,
                computedPosition: window.getComputedStyle(nav).position,
                computedTop: window.getComputedStyle(nav).top,
                computedHeight: window.getComputedStyle(nav).height,
                parentTag: nav.parentElement.tagName,
                parentId: nav.parentElement.id,
                parentClass: nav.parentElement.className
            };
        }''')
        print(f"Parent: <{res['parentTag']} id='{res['parentId']}' class='{res['parentClass']}'>")
        print(f"Computed position: {res['computedPosition']}, top: {res['computedTop']}, height: {res['computedHeight']}")
        for m in res['matched']:
            print(f"  [{m['href']}] {m['selector']} -> {m['cssText'][:120]}")
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
