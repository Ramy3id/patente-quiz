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
            page.wait_for_timeout(400)
    except Exception:
        pass

    # 1. Screenshot of the whole top area:
    # Full width return button, centered header controls, clearly visible active star button, and compact 3-tool buttons
    page.screenshot(path=f"{artifact_dir}/verified_top_all_fixes.png")

    # 2. Scroll to bottom navigation to show السابق and التالي
    page.evaluate("window.scrollTo(0, 450)")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{artifact_dir}/verified_nav_buttons_fixed.png")

    browser.close()

print("Verification screenshots captured successfully!")
