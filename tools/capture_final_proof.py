import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Mobile view (430x932)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    url = "http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20"
    page.goto(url)
    
    # Dismiss GDPR banner
    page.evaluate("() => { localStorage.setItem('cookie_consent', 'accepted'); document.getElementById('cookie-consent-banner')?.remove(); }")
    page.wait_for_timeout(400)

    # Screenshot 1: Mobile Top (Back link, Session header, and the new 3-tool card)
    page.screenshot(path=f"{artifact_dir}/verified_mobile_top_tools.png")

    # Scroll down to show Question, VERO/FALSO centered, and symmetrical Navigation footer
    card = page.query_selector('#qCardSection')
    if card:
        card.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=f"{artifact_dir}/verified_mobile_card_and_nav.png")

    # Answer question to see feedback drawer and active next button
    btn_v = page.query_selector('#btnVero')
    if btn_v:
        btn_v.click()
        page.wait_for_timeout(400)
        page.screenshot(path=f"{artifact_dir}/verified_mobile_answered_feedback.png")

    # 2. Desktop view (900x1000)
    page_d = browser.new_page(viewport={"width": 900, "height": 1000})
    page_d.goto(url)
    page_d.evaluate("() => { localStorage.setItem('cookie_consent', 'accepted'); document.getElementById('cookie-consent-banner')?.remove(); }")
    page_d.wait_for_timeout(400)
    page_d.screenshot(path=f"{artifact_dir}/verified_desktop_layout.png")

    browser.close()

print("Verification screenshots captured successfully!")
