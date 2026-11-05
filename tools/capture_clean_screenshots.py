from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto('http://localhost:8080/interactive_pages/piano-studio.html', wait_until='networkidle')
        page.wait_for_timeout(600)
        
        # Click cookie accept if visible
        try:
            btn = page.locator('button:has-text("قبول ومتابعة")')
            if btn.count() > 0:
                btn.first.click()
                page.wait_for_timeout(400)
        except Exception as e:
            print("Cookie click exception:", e)
            
        page.add_style_tag(content="""
            #cookieConsentBanner, .cookie-banner, [id*="cookie"], [class*="cookie"] {
                display: none !important;
                visibility: hidden !important;
                pointer-events: none !important;
            }
        """)
        
        # Open setup modal
        page.evaluate("() => { if (typeof openPlanSetupModal === 'function') openPlanSetupModal(); }")
        page.wait_for_timeout(400)
        
        # 1. Top
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\modal_top_no_cookie.png')
        
        # 2. Middle (Q2 & Q3)
        page.evaluate("() => { const m = document.getElementById('planSetupModal'); if (m) m.scrollTop = 420; }")
        page.wait_for_timeout(300)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\modal_mid_no_cookie.png')
        
        # 3. Bottom (Q4 and Actions)
        page.evaluate("() => { const m = document.getElementById('planSetupModal'); if (m) m.scrollTop = m.scrollHeight; }")
        page.wait_for_timeout(300)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\modal_bottom_no_cookie.png')
        
        print("Captured 3 no-cookie screenshots!")
        browser.close()

if __name__ == '__main__':
    test()
