from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://localhost:8080/interactive_pages/scheda-esame.html')
        page.wait_for_timeout(1000)
        
        # Switch to official mode
        page.click('#btnSkinMoto')
        page.wait_for_timeout(400)
        
        # 1. Check in Dark Mode
        summary_box = page.locator('#motoSummaryAnswered').bounding_box()
        label_box = page.locator('.moto-summary-label').bounding_box()
        count_box = page.locator('.moto-summary-count').bounding_box()
        
        print('=== DARK MODE MOTO SUMMARY ===')
        print(f"Summary box: {summary_box}")
        print(f"Label box: {label_box}")
        print(f"Count box: {count_box}")
        
        # Capture zoomed screenshot of nav row in dark mode
        page.locator('.moto-nav-row').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_nav_row_dark.png')
        
        # 2. Answer question 1 (Click VERO) and check counter update
        page.click('#btnMotoVero')
        page.wait_for_timeout(300)
        count_text = page.locator('.moto-summary-count').inner_text()
        print(f"Count text after answer: '{count_text}'")
        
        # 3. Check in Light Mode
        page.evaluate('() => document.documentElement.classList.add("light")')
        page.wait_for_timeout(400)
        
        page.locator('.moto-nav-row').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_nav_row_light.png')
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_full_light_final.png')
        
        browser.close()
    print('Playwright test completed.')

if __name__ == '__main__':
    run()
