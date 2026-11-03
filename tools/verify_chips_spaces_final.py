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
    
    # 1. Light Mode verification
    page.evaluate('window.applyTheme && window.applyTheme("light")')
    page.wait_for_timeout(300)
    
    texts = page.evaluate('''() => {
        const subs = document.querySelectorAll(".chip-sub");
        return Array.from(subs).map(s => s.innerText);
    }''')
    print('Chip sub texts in Light Mode:', texts)
    
    # Visual check on "02 - 10":
    order_info = page.evaluate('''() => {
        const el = document.querySelectorAll(".chip-sub")[1]; // "02 - 10"
        const range1 = document.createRange();
        range1.setStart(el.firstChild, 0);
        range1.setEnd(el.firstChild, 2); // "02"
        const rect02 = range1.getBoundingClientRect();
        
        const range2 = document.createRange();
        range2.setStart(el.firstChild, el.firstChild.length - 2);
        range2.setEnd(el.firstChild, el.firstChild.length); // "10"
        const rect10 = range2.getBoundingClientRect();
        
        return {
            text: el.innerText,
            x_02: rect02.x,
            x_10: rect10.x,
            startAtRight: rect02.x > rect10.x // In Arabic RTL, starting number should be on the right (higher X)
        };
    }''')
    print('Visual order info:', order_info)
    
    # Screenshot filter chips in Light Mode
    page.locator('.filter-chips').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_chips_spaces_light.png')
    page.locator('.controls-bar').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_controls_bar_spaces_light.png')

    # 2. Dark Mode verification
    page.evaluate('window.applyTheme && window.applyTheme("dark")')
    page.wait_for_timeout(300)
    page.locator('.filter-chips').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_chips_spaces_dark.png')

    browser.close()
    print("Verification completed successfully!")
