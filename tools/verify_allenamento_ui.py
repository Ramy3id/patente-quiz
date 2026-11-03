import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Mobile Light Mode
    page = browser.new_page(viewport={"width": 430, "height": 932})
    url = "http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20"
    page.goto(url)
    page.evaluate("() => { localStorage.setItem('cookie_consent', 'accepted'); document.getElementById('cookie-consent-banner')?.remove(); }")
    page.wait_for_timeout(500)
    
    # Top + tools + question card screenshot
    page.screenshot(path=f"{artifact_dir}/allenamento_mobile_light_top.png")

    # Scroll down to see VERO/FALSO and navigation footer
    page.evaluate("window.scrollTo(0, 350)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{artifact_dir}/allenamento_mobile_light_bottom.png")

    # 2. Test answering a question (e.g. click FALSO) to see feedback drawer and active next button
    btn_falso = page.query_selector('#btnFalso')
    if btn_falso:
        btn_falso.click()
        page.wait_for_timeout(400)
        page.screenshot(path=f"{artifact_dir}/allenamento_mobile_light_answered.png")

    # 3. Mobile Dark Mode
    page.evaluate("() => { if(window.setTheme) window.setTheme('dark'); else document.documentElement.className = 'dark'; }")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{artifact_dir}/allenamento_mobile_dark.png")

    # 4. Desktop Viewport (900px)
    page_desktop = browser.new_page(viewport={"width": 900, "height": 900})
    page_desktop.goto(url)
    page_desktop.evaluate("() => { localStorage.setItem('cookie_consent', 'accepted'); document.getElementById('cookie-consent-banner')?.remove(); }")
    page_desktop.wait_for_timeout(500)
    page_desktop.screenshot(path=f"{artifact_dir}/allenamento_desktop_overview.png")

    browser.close()

print("All test screenshots captured!")
