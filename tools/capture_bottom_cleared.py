from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto('http://localhost:8080/interactive_pages/piano-studio.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        
        page.add_style_tag(content="""
            #cookieConsentBanner, .cookie-banner, [id*="cookie"], [class*="cookie"] {
                display: none !important;
            }
        """)
        
        page.evaluate("() => { if (typeof openPlanSetupModal === 'function') openPlanSetupModal(); }")
        page.wait_for_timeout(400)
        
        page.evaluate("() => { const m = document.getElementById('planSetupModal'); if (m) m.scrollTop = m.scrollHeight; }")
        page.wait_for_timeout(300)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\modal_bottom_cleared.png')
        
        print("Captured modal_bottom_cleared.png")
        browser.close()

if __name__ == '__main__':
    test()
