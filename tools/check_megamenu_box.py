from playwright.sync_api import sync_playwright
from test_navbar_icon_reorder import CSS_TEST

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
    page.add_style_tag(content=CSS_TEST)
    page.evaluate("() => { const b = document.getElementById('btnToggleChaptersMenu'); if(b) b.click(); }")
    box = page.evaluate("() => { const m = document.getElementById('chaptersDropdownMenu'); const r = m.getBoundingClientRect(); return {left: r.left, right: r.right, width: r.width, top: r.top, bottom: r.bottom}; }")
    print('Megamenu BoundingBox:', box)
    browser.close()
