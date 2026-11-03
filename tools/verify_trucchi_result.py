import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Mobile Light Mode (390x844)
        ctx_mobile_light = browser.new_context(viewport={'width': 390, 'height': 844})
        p_ml = ctx_mobile_light.new_page()
        p_ml.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        p_ml.goto('http://localhost:8080/interactive_pages/trucchi-esame.html')
        p_ml.wait_for_timeout(800)
        p_ml.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\trucchi_mobile_light_verified.png')
        
        # 2. Mobile Dark Mode (390x844)
        ctx_mobile_dark = browser.new_context(viewport={'width': 390, 'height': 844})
        p_md = ctx_mobile_dark.new_page()
        p_md.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'dark');
            document.documentElement.className = 'dark';
        """)
        p_md.goto('http://localhost:8080/interactive_pages/trucchi-esame.html')
        p_md.wait_for_timeout(800)
        p_md.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\trucchi_mobile_dark_verified.png')

        # 3. Small Mobile Screen (360x740)
        ctx_mobile_small = browser.new_context(viewport={'width': 360, 'height': 740})
        p_ms = ctx_mobile_small.new_page()
        p_ms.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        p_ms.goto('http://localhost:8080/interactive_pages/trucchi-esame.html')
        p_ms.wait_for_timeout(800)
        p_ms.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\trucchi_mobile_small_360.png')

        # 4. Desktop (1200x800)
        ctx_desktop = browser.new_context(viewport={'width': 1200, 'height': 800})
        p_desk = ctx_desktop.new_page()
        p_desk.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        p_desk.goto('http://localhost:8080/interactive_pages/trucchi-esame.html')
        p_desk.wait_for_timeout(800)
        p_desk.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\trucchi_desktop_verified.png')

        # Check scroll width vs client width on tabs nav
        scroll_info = p_ml.evaluate("""() => {
            const nav = document.querySelector('.tr-tabs-nav');
            return {
                scrollWidth: nav.scrollWidth,
                clientWidth: nav.clientWidth,
                hasHorizontalScroll: nav.scrollWidth > nav.clientWidth,
                tabCount: nav.querySelectorAll('.tr-tab-btn').length
            };
        }""")
        print("Tabs Nav info:", scroll_info)
        browser.close()

if __name__ == '__main__':
    verify()
