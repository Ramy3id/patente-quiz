from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto('http://localhost:8080/Capitoli_Divisi/parole-quiz.html', wait_until='networkidle')
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\parole_mobile_test.png', full_page=True)
        print("Captured parole_mobile_test.png")
        browser.close()

if __name__ == '__main__':
    test()
