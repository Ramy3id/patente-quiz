import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    page.goto("http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20")
    page.wait_for_selector('.tr-choice-grid', timeout=10000)

    # Let's inspect styles
    res = page.evaluate("""() => {
        const el = document.querySelector('.tr-choice-grid');
        const v = document.getElementById('btnVero');
        const f = document.getElementById('btnFalso');
        const card = el.closest('.tr-question-card') || el.parentElement;
        return {
            grid: {
                display: getComputedStyle(el).display,
                width: getComputedStyle(el).width,
                gridTemplateColumns: getComputedStyle(el).gridTemplateColumns,
                direction: getComputedStyle(el).direction,
                margin: getComputedStyle(el).margin,
                padding: getComputedStyle(el).padding
            },
            vero: {
                width: getComputedStyle(v).width,
                flex: getComputedStyle(v).flex,
                margin: getComputedStyle(v).margin
            },
            falso: {
                width: getComputedStyle(f).width,
                flex: getComputedStyle(f).flex,
                margin: getComputedStyle(f).margin
            },
            card: {
                width: getComputedStyle(card).width,
                direction: getComputedStyle(card).direction
            }
        };
    }""")
    import json
    print(json.dumps(res, indent=2))
    browser.close()
