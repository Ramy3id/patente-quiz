import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    
    # Pre-accept GDPR
    page.add_init_script('localStorage.setItem("patente_gdpr_consent", "true");')
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_load_state('networkidle')
    
    # Scroll to controls bar
    page.locator('.controls-bar').scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    
    buttons = page.locator('.chip-btn')
    for i in range(buttons.count()):
        btn = buttons.nth(i)
        cat = btn.get_attribute('data-cat')
        title = btn.locator('.chip-title').inner_text()
        rect = btn.bounding_box()
        el_at_point = page.evaluate('''(rect) => {
            const x = rect.x + rect.width / 2;
            const y = rect.y + rect.height / 2;
            const el = document.elementFromPoint(x, y);
            return el ? el.tagName + '.' + el.className : 'null';
        }''', rect)
        print(f"With GDPR accepted -> Btn {i}: cat={cat}, title={title}, elementAtPoint={el_at_point}")
        
    browser.close()
