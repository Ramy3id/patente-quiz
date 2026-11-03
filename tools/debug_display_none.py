import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.add_init_script('localStorage.setItem("patente_gdpr_consent", "accepted");')
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_load_state('networkidle')
    
    # Click segnali
    page.click('.chip-btn[data-cat="segnali"]')
    page.wait_for_timeout(300)
    
    # Inspect card 1 (Capitolo 01 - should be hidden!)
    card1_info = page.evaluate('''() => {
        const card1 = document.querySelector(".chapter-card");
        return {
            inlineDisplay: card1.style.display,
            computedDisplay: window.getComputedStyle(card1).display,
            cat: card1.dataset.cat
        };
    }''')
    print('Card 1 info after clicking segnali:', card1_info)
    browser.close()
