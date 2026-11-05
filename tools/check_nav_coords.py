from playwright.sync_api import sync_playwright
from test_navbar_icon_reorder import CSS_TEST

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
    page.add_style_tag(content=CSS_TEST)
    info = page.evaluate("""() => {
        const act = document.querySelector('.nav-desktop-actions').getBoundingClientRect();
        const tabs = document.querySelector('.nav-desktop-tabs').getBoundingClientRect();
        const brand = document.querySelector('.nav-brand-group').getBoundingClientRect();
        const nav = document.getElementById('globalPortalNav').getBoundingClientRect();
        return {
            nav: {left: nav.left, right: nav.right},
            actions: {left: act.left, right: act.right, width: act.width},
            tabs: {left: tabs.left, right: tabs.right, width: tabs.width},
            brand: {left: brand.left, right: brand.right, width: brand.width}
        };
    }""")
    print('Layout coordinates:', info)
    browser.close()
