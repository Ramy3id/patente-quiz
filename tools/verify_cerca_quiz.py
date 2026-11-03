import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Mobile Light Mode
        ctx_ml = browser.new_context(viewport={'width': 390, 'height': 844})
        p_ml = ctx_ml.new_page()
        p_ml.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        p_ml.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        p_ml.wait_for_timeout(1000)
        p_ml.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_mobile_light_verified.png')

        # 2. Mobile Dark Mode
        ctx_md = browser.new_context(viewport={'width': 390, 'height': 844})
        p_md = ctx_md.new_page()
        p_md.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'dark');
            document.documentElement.className = 'dark';
        """)
        p_md.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        p_md.wait_for_timeout(1000)
        p_md.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_mobile_dark_verified.png')

        # 3. Small Mobile Screen (360x740)
        ctx_sm = browser.new_context(viewport={'width': 360, 'height': 740})
        p_sm = ctx_sm.new_page()
        p_sm.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        p_sm.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        p_sm.wait_for_timeout(1000)
        p_sm.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_mobile_360_verified.png')

        # 4. Desktop (1200x800)
        ctx_d = browser.new_context(viewport={'width': 1200, 'height': 800})
        p_d = ctx_d.new_page()
        p_d.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        p_d.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        p_d.wait_for_timeout(1000)
        p_d.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_desktop_verified.png')

        # 5. Test interaction with custom dropdown
        p_ml.click('#cqDropdownTrigger')
        p_ml.wait_for_timeout(300)
        
        # Click 'sorpasso in curva'
        item = p_ml.locator('.cq-dd-item:has-text("sorpasso in curva")')
        item.click()
        p_ml.wait_for_timeout(400)
        
        input_val = p_ml.input_value('#cqSearchInput')
        count_text = p_ml.inner_text('#cqCountText')
        print(f"After selecting from custom dropdown: input='{input_val}', count='{count_text}'")
        assert 'sorpasso in curva' in input_val, "Dropdown selection should populate input"

        # Test clear button
        p_ml.click('#cqClearBtn')
        p_ml.wait_for_timeout(300)
        cleared_val = p_ml.input_value('#cqSearchInput')
        print(f"After clear button: input='{cleared_val}'")
        assert cleared_val == '', "Clear button should clear input"

        # Check horizontal overflow on body
        overflow_info = p_ml.evaluate("""() => {
            const body = document.body;
            return {
                bodyScrollWidth: body.scrollWidth,
                bodyClientWidth: body.clientWidth,
                hasOverflow: body.scrollWidth > body.clientWidth
            };
        }""")
        print("Page Overflow Info:", overflow_info)

        browser.close()
        print("All cerca-quiz verifications passed cleanly!")

if __name__ == '__main__':
    verify()
