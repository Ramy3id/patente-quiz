import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    
    # Listen for errors
    errors = []
    page.on('console', lambda msg: print(f"CONSOLE {msg.type}: {msg.text}"))
    page.on('pageerror', lambda exc: print(f"PAGEERROR: {exc}"))
    
    # Pre-accept GDPR
    page.add_init_script('localStorage.setItem("patente_gdpr_consent", "accepted");')
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_load_state('networkidle')
    
    # Scroll to controls bar
    page.locator('.controls-bar').scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    
    print("\n--- Initial State ---")
    active_btn = page.evaluate('document.querySelector(".chip-btn.active") ? document.querySelector(".chip-btn.active").dataset.cat : "none"')
    visible_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card")).filter(c => window.getComputedStyle(c).display !== "none").map(c => c.querySelector(".ch-pill-num").innerText)')
    print(f"Active button: {active_btn}")
    print(f"Visible cards count: {len(visible_cards)}")
    print(f"First 5 visible cards: {visible_cards[:5]}")
    
    # Click on "الإشارات" (segnali)
    print("\n--- Clicking on 'الإشارات' (segnali) ---")
    page.click('.chip-btn[data-cat="segnali"]')
    page.wait_for_timeout(300)
    
    active_btn = page.evaluate('document.querySelector(".chip-btn.active") ? document.querySelector(".chip-btn.active").dataset.cat : "none"')
    visible_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card")).filter(c => window.getComputedStyle(c).display !== "none").map(c => c.querySelector(".ch-pill-num").innerText)')
    print(f"Active button: {active_btn}")
    print(f"Visible cards count: {len(visible_cards)}")
    print(f"Visible cards: {visible_cards}")
    
    # Click on "القواعد" (norme)
    print("\n--- Clicking on 'القواعد' (norme) ---")
    page.click('.chip-btn[data-cat="norme"]')
    page.wait_for_timeout(300)
    active_btn = page.evaluate('document.querySelector(".chip-btn.active") ? document.querySelector(".chip-btn.active").dataset.cat : "none"')
    visible_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card")).filter(c => window.getComputedStyle(c).display !== "none").map(c => c.querySelector(".ch-pill-num").innerText)')
    print(f"Active button: {active_btn}")
    print(f"Visible cards count: {len(visible_cards)}")
    print(f"Visible cards: {visible_cards}")

    # Click on "التقاطعات" (precedenze)
    print("\n--- Clicking on 'التقاطعات' (precedenze) ---")
    page.click('.chip-btn[data-cat="precedenze"]')
    page.wait_for_timeout(300)
    active_btn = page.evaluate('document.querySelector(".chip-btn.active") ? document.querySelector(".chip-btn.active").dataset.cat : "none"')
    visible_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card")).filter(c => window.getComputedStyle(c).display !== "none").map(c => c.querySelector(".ch-pill-num").innerText)')
    print(f"Active button: {active_btn}")
    print(f"Visible cards count: {len(visible_cards)}")
    print(f"Visible cards: {visible_cards}")

    # Click on "السلامة" (sicurezza)
    print("\n--- Clicking on 'السلامة' (sicurezza) ---")
    page.click('.chip-btn[data-cat="sicurezza"]')
    page.wait_for_timeout(300)
    active_btn = page.evaluate('document.querySelector(".chip-btn.active") ? document.querySelector(".chip-btn.active").dataset.cat : "none"')
    visible_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card")).filter(c => window.getComputedStyle(c).display !== "none").map(c => c.querySelector(".ch-pill-num").innerText)')
    print(f"Active button: {active_btn}")
    print(f"Visible cards count: {len(visible_cards)}")
    print(f"Visible cards: {visible_cards}")

    # Click on "الميكانيكا" (meccanica)
    print("\n--- Clicking on 'الميكانيكا' (meccanica) ---")
    page.click('.chip-btn[data-cat="meccanica"]')
    page.wait_for_timeout(300)
    active_btn = page.evaluate('document.querySelector(".chip-btn.active") ? document.querySelector(".chip-btn.active").dataset.cat : "none"')
    visible_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card")).filter(c => window.getComputedStyle(c).display !== "none").map(c => c.querySelector(".ch-pill-num").innerText)')
    print(f"Active button: {active_btn}")
    print(f"Visible cards count: {len(visible_cards)}")
    print(f"Visible cards: {visible_cards}")

    browser.close()
