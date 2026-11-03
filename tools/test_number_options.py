import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    
    # Let's test 3 different options on the page and capture screenshots:
    
    # Option A: Just adding spaces: "02 - 10" (in current RTL)
    page.evaluate('''() => {
        const subs = document.querySelectorAll(".chip-sub");
        if (subs[1]) subs[1].innerText = "02 - 10";
        if (subs[2]) subs[2].innerText = "11 - 13";
        if (subs[3]) subs[3].innerText = "14 - 16";
        if (subs[4]) subs[4].innerText = "17 - 20";
        if (subs[5]) subs[5].innerText = "21 - 25";
    }''')
    page.locator('.filter-chips').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\test_chips_opt_A_spaces_rtl.png')
    
    # Option B: dir="ltr" with spaces: "02 - 10"
    page.evaluate('''() => {
        const subs = document.querySelectorAll(".chip-sub");
        subs.forEach((s, idx) => {
            if (idx > 0) {
                s.style.direction = "ltr";
                s.style.unicodeBidi = "isolate";
            }
        });
    }''')
    page.locator('.filter-chips').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\test_chips_opt_B_spaces_ltr.png')

    # Option C: What does the user want?
    # User said:
    # يعنى بدل من
    # 02 - 10
    # مكتوب
    # 02-10
    # ممكن يكون عدم وجود مسافات (قبل وبعد -) هوة السبب ؟!
    
    browser.close()
    print("Screenshots captured!")
