import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
    page.wait_for_timeout(500)
    styles = page.evaluate("""() => {
        const p = document.getElementById('globalProgressPill');
        const t = document.querySelector('.nav-theme-btn');
        const a = document.getElementById('globalAuthPill');
        const s = document.getElementById('btnOpenGlobalSearch');
        return {
            search: {display: getComputedStyle(s).display, width: getComputedStyle(s).width, visibility: getComputedStyle(s).visibility},
            progress: {display: getComputedStyle(p).display, width: getComputedStyle(p).width, visibility: getComputedStyle(p).visibility, opacity: getComputedStyle(p).opacity},
            auth: {display: getComputedStyle(a).display, width: getComputedStyle(a).width, text: a.innerText},
            theme: {display: getComputedStyle(t).display, width: getComputedStyle(t).width, visibility: getComputedStyle(t).visibility, opacity: getComputedStyle(t).opacity}
        };
    }""")
    print("Computed styles:", styles)
    browser.close()
