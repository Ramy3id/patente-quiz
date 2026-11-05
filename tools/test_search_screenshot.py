import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    page.goto('http://localhost:8080/index.html')
    page.wait_for_timeout(1000)
    
    # Click accept on GDPR banner if present
    btn = page.locator('button:has-text("قبول ومتابعة")')
    if btn.count() > 0:
        btn.click()
        page.wait_for_timeout(500)

    # Click search button
    page.click('#btnOpenMobileSearch')
    page.wait_for_timeout(500)
    
    # Capture Dark mode
    out_dark = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\search_modal_dark_verified.png'
    page.evaluate("() => { document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark'); }")
    page.wait_for_timeout(200)
    page.screenshot(path=out_dark)
    print("Dark mode screenshot saved.")

    # Capture Light mode
    out_light = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\search_modal_light_verified.png'
    page.evaluate("() => { document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light'); }")
    page.wait_for_timeout(200)
    page.screenshot(path=out_light)
    print("Light mode screenshot saved.")

    browser.close()
