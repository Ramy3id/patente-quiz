from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        
        # Scroll to bento tools section
        bento = page.locator('.bento-tools-section')
        if bento.count() > 0:
            bento.first.scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\bento_tools_reordered.png')
            print("Captured bento_tools_reordered.png")
            
        browser.close()

if __name__ == '__main__':
    test()
