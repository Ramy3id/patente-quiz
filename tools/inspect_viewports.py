import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

for w in [430, 768, 1024, 1280]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": w, "height": 900})
        page.goto("http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20")
        page.wait_for_selector('.tr-choice-grid', timeout=10000)
        
        info = page.evaluate("() => { const g = document.querySelector('.tr-choice-grid'); const card = document.querySelector('.tr-question-card') || document.querySelector('main'); const rectG = g.getBoundingClientRect(); const rectC = card.getBoundingClientRect(); return { w: window.innerWidth, cardW: rectC.width, cardL: rectC.left, cardR: rectC.right, gridW: rectG.width, gridL: rectG.left, gridR: rectG.right, gridMargin: window.getComputedStyle(g).margin }; }")
        print(f"Viewport {w}: {info}")
        browser.close()
