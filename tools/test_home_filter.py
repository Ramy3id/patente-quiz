import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    
    # Listen to console errors and exceptions
    errors = []
    page.on('console', lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}"))
    page.on('pageerror', lambda exc: errors.append(f"PAGEERROR: {exc}"))
    
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_load_state('networkidle')
    
    # Count visible cards initially
    initial_visible = page.evaluate('document.querySelectorAll(".chapter-card:not([style*=\'display: none\'])").length')
    print('Initial visible cards:', initial_visible)
    
    # Click on "الإشارات" (segnali)
    print("Clicking on [data-cat='segnali']...")
    page.click('.chip-btn[data-cat="segnali"]')
    page.wait_for_timeout(300)
    
    segnali_visible = page.evaluate('document.querySelectorAll(".chapter-card:not([style*=\'display: none\'])").length')
    active_btn = page.evaluate('document.querySelector(".chip-btn.active") ? document.querySelector(".chip-btn.active").dataset.cat : "none"')
    print('After clicking segnali:')
    print('  Active button:', active_btn)
    print('  Visible cards:', segnali_visible)
    
    # Click on "القواعد" (norme)
    print("Clicking on [data-cat='norme']...")
    page.click('.chip-btn[data-cat="norme"]')
    page.wait_for_timeout(300)
    norme_visible = page.evaluate('document.querySelectorAll(".chapter-card:not([style*=\'display: none\'])").length')
    print('After clicking norme: visible =', norme_visible)
    
    # Click on "التقاطعات" (precedenze)
    print("Clicking on [data-cat='precedenze']...")
    page.click('.chip-btn[data-cat="precedenze"]')
    page.wait_for_timeout(300)
    precedenze_visible = page.evaluate('document.querySelectorAll(".chapter-card:not([style*=\'display: none\'])").length')
    print('After clicking precedenze: visible =', precedenze_visible)

    print('Errors recorded:', errors)
    browser.close()
