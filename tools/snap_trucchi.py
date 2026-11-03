import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def snap():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 390, 'height': 844})
        page = context.new_page()
        page.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
        """)
        page.goto('http://localhost:8080/interactive_pages/trucchi-esame.html')
        page.wait_for_timeout(600)
        
        # Scroll to top to see hero and tabs
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\trucchi_mobile_clean.png')
        print("Captured clean mobile screenshot!")
        browser.close()

if __name__ == '__main__':
    snap()
