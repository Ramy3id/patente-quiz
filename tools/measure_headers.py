import asyncio
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.async_api import async_playwright

PAGES = [
    ("Home", "http://localhost:8080/Capitoli_Divisi/index.html"),
    ("Radar", "http://localhost:8080/interactive_pages/parole-spia.html"),
    ("Exam", "http://localhost:8080/interactive_pages/scheda-esame.html"),
    ("Dashboard", "http://localhost:8080/interactive_pages/dashboard.html")
]

MEASURE_JS = """
() => {
    const nav = document.getElementById('globalPortalNav') || document.querySelector('.unified-portal-nav');
    const body = document.body;
    const navRect = nav ? nav.getBoundingClientRect() : null;
    const navStyle = nav ? window.getComputedStyle(nav) : null;
    const bodyStyle = window.getComputedStyle(body);
    
    // Find first visible content element after nav
    let firstContent = null;
    let firstRect = null;
    if (nav) {
        let el = nav.nextElementSibling;
        while (el) {
            const s = window.getComputedStyle(el);
            if (s.display !== 'none' && s.visibility !== 'hidden' && el.offsetHeight > 0) {
                firstContent = el;
                firstRect = el.getBoundingClientRect();
                break;
            }
            el = el.nextElementSibling;
        }
        if (!firstContent && nav.parentElement) {
            let parentSibling = nav.parentElement.nextElementSibling;
            while (parentSibling) {
                const s = window.getComputedStyle(parentSibling);
                if (s.display !== 'none' && s.visibility !== 'hidden' && parentSibling.offsetHeight > 0) {
                    firstContent = parentSibling;
                    firstRect = parentSibling.getBoundingClientRect();
                    break;
                }
                parentSibling = parentSibling.nextElementSibling;
            }
        }
    }
    
    return {
        bodyPaddingTop: bodyStyle.paddingTop,
        bodyMarginTop: bodyStyle.marginTop,
        navExists: !!nav,
        navTag: nav ? nav.tagName : null,
        navPosition: navStyle ? navStyle.position : null,
        navTop: navStyle ? navStyle.top : null,
        navHeight: navStyle ? navStyle.height : null,
        navMarginTop: navStyle ? navStyle.marginTop : null,
        navMarginBottom: navStyle ? navStyle.marginBottom : null,
        navPaddingTop: navStyle ? navStyle.paddingTop : null,
        navPaddingBottom: navStyle ? navStyle.paddingBottom : null,
        navBoundingRect: navRect ? {
            top: navRect.top,
            bottom: navRect.bottom,
            height: navRect.height,
            width: navRect.width
        } : null,
        firstContentTag: firstContent ? firstContent.tagName : null,
        firstContentId: firstContent ? firstContent.id : null,
        firstContentClass: firstContent ? firstContent.className : null,
        firstContentMarginTop: firstContent ? window.getComputedStyle(firstContent).marginTop : null,
        firstContentTop: firstRect ? firstRect.top : null,
        gapBetweenNavAndContent: (navRect && firstRect) ? (firstRect.top - navRect.bottom) : null
    };
}
"""

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 375, 'height': 812})
        for name, url in PAGES:
            await page.goto(url)
            await page.wait_for_timeout(1000)
            res = await page.evaluate(MEASURE_JS)
            print(f"=== {name} ({url}) ===")
            print(f"  Nav exists: {res['navExists']} (position: {res['navPosition']}, top: {res['navTop']})")
            print(f"  Nav Rect: top={res['navBoundingRect']['top']}px, bottom={res['navBoundingRect']['bottom']}px, height={res['navBoundingRect']['height']}px")
            print(f"  Nav styles: height={res['navHeight']}, mt={res['navMarginTop']}, mb={res['navMarginBottom']}, pt={res['navPaddingTop']}, pb={res['navPaddingBottom']}")
            print(f"  Body styles: pt={res['bodyPaddingTop']}, mt={res['bodyMarginTop']}")
            print(f"  First Content: <{res['firstContentTag']} id='{res['firstContentId']}' class='{res['firstContentClass']}'>")
            print(f"    firstContentTop={res['firstContentTop']}px, firstContentMarginTop={res['firstContentMarginTop']}")
            print(f"    👉 GAP Between Nav and First Content: {res['gapBetweenNavAndContent']}px")
            print()
            
            # Take screenshot of header area (top 150px)
            await page.screenshot(
                path=f"C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/header_measure_{name.lower()}.png",
                clip={'x': 0, 'y': 0, 'width': 375, 'height': 200}
            )
        await b.close()

if __name__ == '__main__':
    asyncio.run(run())
