import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Mobile Drawer View
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    page.goto('http://localhost:8080/index.html')
    page.wait_for_timeout(600)
    
    # Dismiss GDPR banner
    page.evaluate("""() => {
        localStorage.setItem('patente_gdpr_consent', 'accepted');
        const b = document.getElementById('patenteGdprBanner');
        if (b) b.remove();
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    }""")
    page.wait_for_timeout(300)
    
    # Open mobile drawer using the correct ID #btnToggleMobileDrawer
    page.click('#btnToggleMobileDrawer')
    page.wait_for_timeout(500)
    out_drawer = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\unified_icons_drawer.png'
    page.screenshot(path=out_drawer)
    print("Drawer screenshot saved.")
    
    # Close drawer and open Search Modal
    page.click('#btnCloseMobileDrawer')
    page.wait_for_timeout(400)
    page.click('#btnOpenMobileSearch')
    page.wait_for_timeout(500)
    out_search = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\unified_icons_search.png'
    page.screenshot(path=out_search)
    print("Search modal screenshot saved.")
    
    # Close search and scroll to Footer
    page.click('#btnCloseGlobalSearch')
    page.wait_for_timeout(400)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(400)
    out_footer = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\unified_icons_footer.png'
    page.screenshot(path=out_footer)
    print("Footer screenshot saved.")

    browser.close()
