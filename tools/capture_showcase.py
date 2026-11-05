import os
from playwright.sync_api import sync_playwright

SHOWCASE_HTML = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\navbar_proposals_showcase.html"
OUT_IMG = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\desktop_navbar_comparison_board.png"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Viewport wide enough to render the whole board cleanly
        context = browser.new_context(viewport={"width": 1440, "height": 2600}, device_scale_factor=1.5)
        page = context.new_page()
        page.goto(f"file:///{SHOWCASE_HTML}", wait_until='networkidle')
        page.wait_for_timeout(600)
        page.screenshot(path=OUT_IMG, full_page=True)
        print("Captured desktop_navbar_comparison_board.png successfully!")
        browser.close()

if __name__ == '__main__':
    run()
