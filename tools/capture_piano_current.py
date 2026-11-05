from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto('http://localhost:8080/interactive_pages/piano-studio.html', wait_until='networkidle')
        # Open setup modal
        page.evaluate("() => { if (typeof openPlanSetupModal === 'function') openPlanSetupModal(); }")
        page.wait_for_timeout(300)
        
        # Scroll down to bottom
        page.evaluate("() => { const m = document.getElementById('planSetupModal'); if (m) m.scrollTop = m.scrollHeight; }")
        page.wait_for_timeout(300)
        
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\piano_modal_bottom_current.png')
        print("Captured piano_modal_bottom_current.png")
        browser.close()

if __name__ == '__main__':
    test()
