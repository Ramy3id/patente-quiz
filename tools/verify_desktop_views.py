from playwright.sync_api import sync_playwright

def test_desktop():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Desktop 1440x900
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        
        # 1. Test index.html desktop
        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\desktop_index_check.png')
        print("Captured desktop_index_check.png")
        
        # 2. Test piano-studio.html desktop
        page.goto('http://localhost:8080/interactive_pages/piano-studio.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\desktop_piano_check.png')
        print("Captured desktop_piano_check.png")
        
        # 3. Test piano-studio.html modal open on desktop
        page.evaluate("() => { if (typeof openPlanSetupModal === 'function') openPlanSetupModal(); }")
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\desktop_piano_modal_check.png')
        print("Captured desktop_piano_modal_check.png")
        
        # 4. Test parole-quiz.html desktop
        page.goto('http://localhost:8080/Capitoli_Divisi/parole-quiz.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\desktop_parole_check.png')
        print("Captured desktop_parole_check.png")
        
        browser.close()

if __name__ == '__main__':
    test_desktop()
