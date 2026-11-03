import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Mobile 390x844 Light
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        page = ctx.new_page()
        page.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        page.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        page.wait_for_timeout(800)
        
        # Click dropdown trigger to OPEN it
        page.click('#cqDropdownTrigger')
        page.wait_for_timeout(400)
        
        # Check bounds of menu
        menu_bounds = page.evaluate("""() => {
            const menu = document.getElementById('cqPopularMenu');
            const rect = menu.getBoundingClientRect();
            return {
                left: rect.left,
                right: rect.right,
                width: rect.width,
                viewportWidth: window.innerWidth,
                isInsideViewport: rect.left >= 0 && rect.right <= window.innerWidth
            };
        }""")
        print("Menu bounds check:", menu_bounds)
        assert menu_bounds['isInsideViewport'], "Menu must be strictly inside viewport!"
        
        # Take screenshot of OPEN custom dropdown
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_custom_dropdown_open.png')
        
        # Click an item inside dropdown: 'frizione'
        item = page.locator('.cq-dd-item:has-text("frizione")')
        item.click()
        page.wait_for_timeout(400)
        
        # Check that menu closed and input is populated
        input_val = page.input_value('#cqSearchInput')
        is_open = page.is_visible('#cqPopularMenu')
        print(f"After click: is_open={is_open}, input='{input_val}'")
        assert not is_open, "Menu should be closed after selection"
        assert input_val == 'frizione', "Input value should be 'frizione'"
        
        # Take screenshot after selection
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_custom_dropdown_selected.png')
        
        # Also test on Dark Mode
        page.evaluate("document.documentElement.className = 'dark'; localStorage.setItem('patente_theme', 'dark');")
        page.click('#cqDropdownTrigger')
        page.wait_for_timeout(300)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_custom_dropdown_dark_open.png')

        browser.close()
        print("Custom dropdown test passed 100%!")

if __name__ == '__main__':
    test()
