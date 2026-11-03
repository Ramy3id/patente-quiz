import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    url = "http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20"
    page.goto(url)

    # Click accept on GDPR
    try:
        btn_acc = page.wait_for_selector('button:has-text("قبول ومتابعة")', timeout=3000)
        if btn_acc:
            btn_acc.click()
            page.wait_for_timeout(500)
    except Exception:
        pass

    # Screenshot 1: Mobile Top Tools strip
    tools = page.query_selector('.tr-smart-tools-card')
    if tools:
        tools.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        page.screenshot(path=f"{artifact_dir}/clean_mobile_smart_tools.png")

    # Screenshot 2: Scroll to VERO/FALSO buttons and navigation
    vf = page.query_selector('.tr-choice-grid')
    if vf:
        vf.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        page.screenshot(path=f"{artifact_dir}/clean_mobile_vf_and_nav.png")

    # Screenshot 3: Click FALSO to answer, then screenshot feedback + next button
    btn_f = page.query_selector('#btnFalso')
    if btn_f:
        btn_f.click()
        page.wait_for_timeout(400)
        footer = page.query_selector('.tr-card-footer')
        if footer:
            footer.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
        page.screenshot(path=f"{artifact_dir}/clean_mobile_answered_next.png")

    browser.close()

print("Clean mobile screenshots captured!")
