import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def snap():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        page = ctx.new_page()
        page.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        page.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        page.wait_for_timeout(800)
        
        # Scroll to bottom of first card
        page.evaluate("window.scrollTo(0, 680)")
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_card_actions_centered_exact.png')
        browser.close()
        print("Captured exact card actions screenshot!")

if __name__ == '__main__':
    snap()
