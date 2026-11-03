import asyncio
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.async_api import async_playwright

PAGES_TO_TEST = [
    "http://localhost:8080/Capitoli_Divisi/index.html",
    "http://localhost:8080/interactive_pages/scheda-esame.html",
    "http://localhost:8080/interactive_pages/parole-spia.html",
    "http://localhost:8080/interactive_pages/dashboard.html",
    "http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html",
    "http://localhost:8080/interactive_pages/decodificatore-incroci.html",
    "http://localhost:8080/interactive_pages/laboratorio-numeri.html",
    "http://localhost:8080/interactive_pages/piano-studio.html",
    "http://localhost:8080/interactive_pages/zero-mistake.html",
    "http://localhost:8080/interactive_pages/cerca-quiz.html",
    "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"
]

JS_SCAN = """
() => {
    const docWidth = document.documentElement.clientWidth;
    const docScrollWidth = document.documentElement.scrollWidth;
    const bodyScrollWidth = document.body ? document.body.scrollWidth : 0;
    
    // Find any element that actually causes document overflow or sticks out beyond viewport WITHOUT an overflow container
    const uncontainedSpills = [];
    const all = document.querySelectorAll('*');
    for (let el of all) {
        const tag = el.tagName.toLowerCase();
        if (['script', 'style', 'head', 'link', 'meta', 'defs', 'title'].includes(tag)) continue;
        
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) continue;
        
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') continue;
        
        // Check if inside a legitimate scroll/clipped container
        let parent = el.parentElement;
        let isContained = false;
        while (parent && parent !== document.body && parent !== document.documentElement) {
            const ps = window.getComputedStyle(parent);
            if (['hidden', 'auto', 'scroll'].includes(ps.overflowX)) {
                isContained = true;
                break;
            }
            parent = parent.parentElement;
        }
        
        if (!isContained) {
            if (rect.right > docWidth + 1 || rect.left < -1) {
                uncontainedSpills.push({
                    tag,
                    id: el.id,
                    className: (el.className && typeof el.className === 'string') ? el.className.slice(0, 50) : '',
                    rect: { left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width) },
                    text: (el.innerText || '').slice(0, 30).replace(/\\s+/g, ' ')
                });
            }
        }
    }
    
    return {
        docWidth,
        docScrollWidth,
        bodyScrollWidth,
        hasHorizontalDocScroll: docScrollWidth > docWidth || bodyScrollWidth > docWidth,
        uncontainedSpillsCount: uncontainedSpills.length,
        uncontainedSpills: uncontainedSpills.slice(0, 10)
    };
}
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport 375x812 (iPhone standard)
        context = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
        )
        page = await context.new_page()
        
        print("=== PLATFORM-WIDE MOBILE OVERFLOW AUDIT (375x812) ===")
        all_passed = True
        for url in PAGES_TO_TEST:
            page_name = url.split('/')[-2] + '/' + url.split('/')[-1]
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                await page.wait_for_timeout(800)
                res = await page.evaluate(JS_SCAN)
                has_issue = res['hasHorizontalDocScroll'] or res['uncontainedSpillsCount'] > 0
                if has_issue: all_passed = False
                status = "🔴 OVERFLOW" if has_issue else "🟢 100% OK"
                print(f"{status} | {page_name:<40} | doc: {res['docScrollWidth']}px, body: {res['bodyScrollWidth']}px | Spills: {res['uncontainedSpillsCount']}")
                if res['uncontainedSpillsCount'] > 0:
                    for s in res['uncontainedSpills']:
                        print(f"    -> <{s['tag']} class='{s['className']}'> left: {s['rect']['left']}, right: {s['rect']['right']}, w: {s['rect']['width']} | '{s['text']}'")
            except Exception as e:
                print(f"❌ Error testing {page_name}: {e}")
                all_passed = False
                
        print(f"\n==========================================")
        print(f"FINAL PLATFORM STATUS: {'🎉 ALL 11 PAGES 100% ZERO OVERFLOW' if all_passed else '⚠️ SOME PAGES NEED ATTENTION'}")
        print(f"==========================================")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
