import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    url = "http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20"
    page.goto(url)

    btn = page.query_selector('#btnCount20')
    info = page.evaluate("""() => {
        const el = document.getElementById('btnCount20');
        const s = window.getComputedStyle(el);
        return {
            bg: s.backgroundColor,
            color: s.color,
            border: s.borderColor,
            classList: Array.from(el.classList)
        };
    }""")
    print("Computed style for #btnCount20 in Light Mode:")
    print(info)
    browser.close()
