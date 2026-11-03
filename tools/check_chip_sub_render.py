import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    
    data = page.evaluate('''() => {
        const subs = document.querySelectorAll(".chip-sub");
        return Array.from(subs).map(s => {
            const cs = window.getComputedStyle(s);
            return {
                text: s.innerText,
                direction: cs.direction,
                unicodeBidi: cs.unicodeBidi
            };
        });
    }''')
    print('Chip sub data:', data)
    
    # Take screenshot of the filter chips
    page.locator('.filter-chips').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\test_chips_sub_current.png')
    browser.close()
