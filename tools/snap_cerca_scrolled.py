import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def snap_scrolled():
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
        
        # Select an option so search input has text and clear button is visible
        page.select_option('#cqPopularSelect', value='sorpasso in curva')
        page.wait_for_timeout(500)
        
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_mobile_with_search.png')
        
        # Scroll to see the full filter panel and results
        page.evaluate("window.scrollTo(0, 160)")
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cerca_mobile_filter_panel_scrolled.png')
        
        browser.close()
        print("Captured scrolled mobile screenshots!")

if __name__ == '__main__':
    snap_scrolled()
