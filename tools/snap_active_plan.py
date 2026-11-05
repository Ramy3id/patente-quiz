import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    page.wait_for_load_state('networkidle')
    
    # Click "ابدأ بالخطة الموصى بها فوراً"
    page.click('.sp-quick-start')
    page.wait_for_timeout(500)
    
    # 1. Top of active plan page
    page.screenshot(path=f'{output_dir}\\piano_active_mobile_top.png')
    
    # 2. Scroll 600px
    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_active_mobile_mid.png')

    # 3. Scroll 1200px
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_active_mobile_bottom.png')

    # 4. Desktop active plan page
    desk = browser.new_page(viewport={'width': 1200, 'height': 900})
    desk.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    desk.wait_for_load_state('networkidle')
    desk.click('.sp-quick-start')
    desk.wait_for_timeout(500)
    desk.screenshot(path=f'{output_dir}\\piano_active_desktop_top.png')

    browser.close()
    print("Captured active plan screenshots.")
