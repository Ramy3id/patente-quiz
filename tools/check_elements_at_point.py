import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    
    # Track all clicks and events
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_load_state('networkidle')
    
    # Check if element at point is the button
    buttons = page.locator('.chip-btn')
    count = buttons.count()
    print(f"Total chip buttons: {count}")
    
    for i in range(count):
        btn = buttons.nth(i)
        cat = btn.get_attribute('data-cat')
        title = btn.locator('.chip-title').inner_text()
        rect = btn.bounding_box()
        # Test element at point
        el_at_point = page.evaluate('''(rect) => {
            const x = rect.x + rect.width / 2;
            const y = rect.y + rect.height / 2;
            const el = document.elementFromPoint(x, y);
            return el ? el.tagName + '.' + el.className : 'null';
        }''', rect)
        print(f"Btn {i}: cat={cat}, title={title}, rect={rect}, elementAtPoint={el_at_point}")
        
    browser.close()
