import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    
    # Check default "02-10"
    def check_sub_visual():
        return page.evaluate('''() => {
            const el = document.querySelectorAll(".chip-sub")[1]; // "02-10"
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
                visualOrder: rect02.x < rect10.x ? "02 is on LEFT, 10 is on RIGHT" : "10 is on LEFT, 02 is on RIGHT"
            };
        }''')
    
    print("Default:")
    print(check_sub_visual())
    
    # Now set spaces without dir=ltr: "02 - 10"
    page.evaluate('document.querySelectorAll(".chip-sub")[1].innerText = "02 - 10";')
    print("With spaces '02 - 10' (no explicit dir):")
    print(check_sub_visual())
    
    # Now set dir="ltr" with spaces: "02 - 10"
    page.evaluate('document.querySelectorAll(".chip-sub")[1].style.direction = "ltr";')
    print("With dir='ltr' and spaces:")
    print(check_sub_visual())

    browser.close()
