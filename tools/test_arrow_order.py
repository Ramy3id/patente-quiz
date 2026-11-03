import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://localhost:8080/interactive_pages/decodificatore-incroci.html')
    page.wait_for_load_state('networkidle')
    
    # Check current arrow boxes
    info = page.evaluate('''() => {
        const wrap = document.querySelector(".sim-arrows-wrap");
        const prevBtn = wrap.querySelectorAll("button")[0];
        const counter = document.getElementById("simNavCounter");
        const nextBtn = wrap.querySelectorAll("button")[1];
        
        return {
            prevBtnHTML: prevBtn.innerHTML,
            nextBtnHTML: nextBtn.innerHTML,
            prevRect: prevBtn.getBoundingClientRect(),
            counterRect: counter.getBoundingClientRect(),
            nextRect: nextBtn.getBoundingClientRect()
        };
    }''')
    print('Current info:', info)
    browser.close()
