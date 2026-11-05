import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_timeout(500)
    
    fav = page.evaluate("() => document.querySelector('link[rel=\"icon\"]').href")
    apple = page.evaluate("() => document.querySelector('link[rel=\"apple-touch-icon\"]').href")
    print("FAVICON HREF:", fav)
    print("APPLE ICON HREF:", apple)
    browser.close()
