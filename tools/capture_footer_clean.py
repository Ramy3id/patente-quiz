from playwright.sync_api import sync_playwright

def test_footer():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        
        # Scroll to bottom to view footer
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(300)
        
        footer = page.locator('#globalPortalFooter')
        if footer.count() > 0:
            footer.first.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\footer_clean_verified.png')
            print("Captured footer_clean_verified.png")
            
        browser.close()

if __name__ == '__main__':
    test_footer()
