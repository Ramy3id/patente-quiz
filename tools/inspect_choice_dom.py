import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    page.goto("http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20")
    page.wait_for_selector('.tr-choice-grid', timeout=10000)
    
    html = page.evaluate("() => document.querySelector('.tr-choice-grid').outerHTML")
    print("Choice grid HTML:")
    print(html)
    
    parent_html = page.evaluate("() => document.querySelector('.tr-choice-grid').parentElement.outerHTML")
    print("\nParent HTML length:", len(parent_html))
    # print around tr-choice-grid in parent
    idx = parent_html.find('tr-choice-grid')
    print(parent_html[idx-100:idx+600])

    browser.close()
