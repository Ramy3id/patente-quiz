import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.add_init_script('localStorage.setItem("patente_gdpr_consent", "accepted");')
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_load_state('networkidle')
    page.evaluate('window.applyTheme && window.applyTheme("light")')
    
    # 1. Update text to have spaces "02 - 10" with default RTL inheritance
    page.evaluate('''() => {
        const subs = document.querySelectorAll(".chip-sub");
        if (subs[1]) subs[1].innerText = "02 - 10";
        if (subs[2]) subs[2].innerText = "11 - 13";
        if (subs[3]) subs[3].innerText = "14 - 16";
        if (subs[4]) subs[4].innerText = "17 - 20";
        if (subs[5]) subs[5].innerText = "21 - 25";
    }''')
    page.locator('.filter-chips').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_chips_spaces_rtl.png')
    
    # Check visual positions of numbers in RTL
    pos_rtl = page.evaluate('''() => {
        const sub = document.querySelectorAll(".chip-sub")[1];
        const text = sub.innerText;
        return {
            text: text,
            html: sub.innerHTML
        };
    }''')
    print('RTL with spaces:', pos_rtl)
    
    # 2. What if dir="ltr" is set on .chip-sub?
    page.evaluate('''() => {
        const subs = document.querySelectorAll(".chip-sub");
        subs.forEach((s, idx) => {
            if (idx > 0) {
                s.style.direction = "ltr";
                s.style.display = "inline-block";
            }
        });
    }''')
    page.locator('.filter-chips').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_chips_spaces_ltr.png')
    
    browser.close()
    print("Done testing both.")
