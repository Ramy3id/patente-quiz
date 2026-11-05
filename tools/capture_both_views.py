from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Desktop 1920x1080 (Matches user's exact screen)
        context_dt = browser.new_context(viewport={"width": 1920, "height": 1080})
        page_dt = context_dt.new_page()
        page_dt.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_dt.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_dt.wait_for_timeout(400)
        page_dt.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\desktop_1080_verified.png')
        print("Captured desktop_1080_verified.png")
        context_dt.close()
        
        # 2. Mobile 390x844
        context_mb = browser.new_context(viewport={"width": 390, "height": 844})
        page_mb = context_mb.new_page()
        page_mb.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_mb.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_mb.wait_for_timeout(400)
        page_mb.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\mobile_390_verified.png')
        print("Captured mobile_390_verified.png")
        context_mb.close()
        
        browser.close()

if __name__ == '__main__':
    test()
