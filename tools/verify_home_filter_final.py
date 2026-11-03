import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 375, 'height': 812})
    page = context.new_page()
    page.add_init_script('localStorage.setItem("patente_gdpr_consent", "accepted");')
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_load_state('networkidle')
    
    # Force light mode
    page.evaluate('window.applyTheme && window.applyTheme("light")')
    page.wait_for_timeout(300)
    
    # 1. Filter: الإشارات (02-10)
    page.click('.chip-btn[data-cat="segnali"]')
    page.wait_for_timeout(300)
    segnali_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card:not(.is-hidden)")).map(c => c.querySelector(".ch-pill-num").innerText)')
    print('Segnali cards (count =', len(segnali_cards), '):', segnali_cards)
    
    # Screenshot filtered to segnali
    page.locator('.controls-bar').scroll_into_view_if_needed()
    page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_home_filter_segnali_light.png')
    
    # 2. Filter: التقاطعات (14-16)
    page.click('.chip-btn[data-cat="precedenze"]')
    page.wait_for_timeout(300)
    precedenze_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card:not(.is-hidden)")).map(c => c.querySelector(".ch-pill-num").innerText)')
    print('Precedenze cards (count =', len(precedenze_cards), '):', precedenze_cards)
    page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_home_filter_precedenze_light.png')

    # 3. Filter: الكل (25)
    page.click('.chip-btn[data-cat="all"]')
    page.wait_for_timeout(300)
    all_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card:not(.is-hidden)")).map(c => c.querySelector(".ch-pill-num").innerText)')
    print('All cards (count =', len(all_cards), '):', len(all_cards))
    
    # 4. Search test: "خطر"
    page.fill('#chapter-search', 'خطر')
    page.wait_for_timeout(300)
    search_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card:not(.is-hidden)")).map(c => c.querySelector(".ch-pill-num").innerText)')
    print('Search "خطر" cards:', search_cards)
    page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_home_search_khatar_light.png')

    # Clear search
    page.fill('#chapter-search', '')
    page.wait_for_timeout(200)

    # 5. Dark mode check
    page.evaluate('window.applyTheme && window.applyTheme("dark")')
    page.wait_for_timeout(300)
    page.click('.chip-btn[data-cat="meccanica"]')
    page.wait_for_timeout(300)
    meccanica_cards = page.evaluate('Array.from(document.querySelectorAll(".chapter-card:not(.is-hidden)")).map(c => c.querySelector(".ch-pill-num").innerText)')
    print('Meccanica cards in Dark mode (count =', len(meccanica_cards), '):', meccanica_cards)
    page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_home_filter_meccanica_dark.png')

    browser.close()
    print('Final verification completed successfully!')
