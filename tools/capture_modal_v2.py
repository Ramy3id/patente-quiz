from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto('http://localhost:8080/interactive_pages/piano-studio.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        
        # Open modal
        page.evaluate("() => { if (typeof openPlanSetupModal === 'function') openPlanSetupModal(); }")
        page.wait_for_timeout(400)
        
        # 1. Capture Top
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\modal_top_v2.png')
        print("Captured modal_top_v2.png")
        
        # 2. Scroll to Middle (Q2 & Q3)
        page.evaluate("() => { const m = document.getElementById('planSetupModal'); if (m) m.scrollTop = 450; }")
        page.wait_for_timeout(300)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\modal_mid_v2.png')
        print("Captured modal_mid_v2.png")
        
        # 3. Scroll to Bottom (Q4 and Actions)
        page.evaluate("() => { const m = document.getElementById('planSetupModal'); if (m) m.scrollTop = m.scrollHeight; }")
        page.wait_for_timeout(300)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\modal_bottom_v2.png')
        print("Captured modal_bottom_v2.png")
        
        browser.close()

if __name__ == '__main__':
    test()
