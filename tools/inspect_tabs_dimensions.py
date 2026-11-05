import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
    page.wait_for_timeout(400)
    
    tabs = page.evaluate("""() => {
        const res = [];
        document.querySelectorAll('.nav-desktop-tabs > *').forEach((el, i) => {
            const btn = el.querySelector('.nav-dropdown-tab') || el;
            const r = btn.getBoundingClientRect();
            const cs = getComputedStyle(btn);
            res.push({
                text: btn.innerText.trim().replace(/\\n/g, ' '),
                tag: btn.tagName,
                height: r.height,
                width: r.width,
                boxSizing: cs.boxSizing,
                padding: cs.padding,
                lineHeight: cs.lineHeight,
                border: cs.border
            });
        });
        return res;
    }""")
    for t in tabs:
        print(t)
    browser.close()
