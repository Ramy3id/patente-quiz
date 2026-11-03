import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def check():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        
        page.on('console', lambda msg: print(f"CONSOLE: [{msg.type}] {msg.text}"))
        page.on('pageerror', lambda err: print(f"PAGEERROR: {err}"))
        
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        page.wait_for_timeout(800)
        
        print("Initial is-open:", page.evaluate("() => document.getElementById('cqPopularDropdown').classList.contains('is-open')"))
        
        # Click trigger
        page.click('#cqDropdownTrigger')
        page.wait_for_timeout(300)
        
        print("After click is-open:", page.evaluate("() => document.getElementById('cqPopularDropdown').classList.contains('is-open')"))
        print("Menu display:", page.evaluate("() => window.getComputedStyle(document.getElementById('cqPopularMenu')).display"))
        
        browser.close()

if __name__ == '__main__':
    check()
