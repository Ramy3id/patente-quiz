import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
    res = page.evaluate("""() => {
        const d = document.querySelector('.nav-dropdown-tab');
        const a = document.querySelector('.nav-direct-tab');
        return {
            dropdown_tab: {
                height: getComputedStyle(d).height,
                minHeight: getComputedStyle(d).minHeight,
                padding: getComputedStyle(d).padding
            },
            direct_tab: {
                height: getComputedStyle(a).height,
                minHeight: getComputedStyle(a).minHeight,
                padding: getComputedStyle(a).padding
            }
        };
    }""")
    print("Tab heights comparison:", res)
    browser.close()
