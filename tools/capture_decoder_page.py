import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})

    url = "http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20"
    page.goto(url)
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)

    page.screenshot(path=f"{artifact_dir}/mofakak_3_kotol_screen.png")
    print("Page Title:", page.title())

    browser.close()

print("Screenshot captured successfully!")
