import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
    page.wait_for_timeout(500)
    html = page.evaluate("() => document.querySelector('.nav-desktop-actions').outerHTML")
    print("Desktop actions HTML:\n", html)
    browser.close()
