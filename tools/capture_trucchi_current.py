import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    url = "http://localhost:8080/interactive_pages/trucchi-esame.html"
    page.goto(url)
    
    # Dismiss GDPR
    try:
        btn_acc = page.wait_for_selector('button:has-text("قبول ومتابعة")', timeout=3000)
        if btn_acc:
            btn_acc.click()
            page.wait_for_timeout(400)
    except Exception:
        pass

    page.screenshot(path=f"{artifact_dir}/trucchi_current_mobile.png")

    # Also desktop
    page_d = browser.new_page(viewport={"width": 1000, "height": 900})
    page_d.goto(url)
    try:
        btn_acc = page_d.wait_for_selector('button:has-text("قبول ومتابعة")', timeout=2000)
        if btn_acc:
            btn_acc.click()
            page_d.wait_for_timeout(300)
    except Exception:
        pass
    page_d.screenshot(path=f"{artifact_dir}/trucchi_current_desktop.png")

    browser.close()

print("Current screenshots taken!")
