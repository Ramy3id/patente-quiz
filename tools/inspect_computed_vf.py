import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    page.goto("http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20")
    page.wait_for_selector('.tr-choice-grid', timeout=10000)
    
    grid = page.query_selector('.tr-choice-grid')
    box_grid = grid.bounding_box()
    print("Grid box:", box_grid)

    btn_v = page.query_selector('#btnVero')
    btn_f = page.query_selector('#btnFalso')
    print("Vero box:", btn_v.bounding_box())
    print("Falso box:", btn_f.bounding_box())
    
    card = page.query_selector('#questionCard')
    print("Card box:", card.bounding_box())

    style_grid = page.evaluate("() => { const el = document.querySelector('.tr-choice-grid'); const s = window.getComputedStyle(el); return { display: s.display, width: s.width, maxWidth: s.maxWidth, margin: s.margin, justifyContent: s.justifyContent }; }")
    print("Grid computed style:", style_grid)

    browser.close()
