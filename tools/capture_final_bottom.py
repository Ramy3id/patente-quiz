from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.goto('http://localhost:8080/interactive_pages/piano-studio.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        
        # Open modal
        page.evaluate("() => { if (typeof openPlanSetupModal === 'function') openPlanSetupModal(); }")
        page.wait_for_timeout(400)
        
        page.evaluate("() => { const m = document.getElementById('planSetupModal'); if (m) m.scrollTop = m.scrollHeight; }")
        page.wait_for_timeout(300)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\final_bottom_view.png')
        
        print("Captured final_bottom_view.png!")
        browser.close()

if __name__ == '__main__':
    test()
