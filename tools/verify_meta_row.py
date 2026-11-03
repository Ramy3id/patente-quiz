from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://localhost:8080/interactive_pages/scheda-esame.html')
        
        # Check in light mode
        page.evaluate('() => document.documentElement.classList.add("light")')
        page.click('#btnSkinMoto')
        page.wait_for_timeout(500)
        
        badge = page.locator('#motoQuestionBadge').bounding_box()
        flag = page.locator('#btnMotoFlag').bounding_box()
        
        print(f"Badge height: {badge['height']:.1f}px")
        print(f"Flag height: {flag['height']:.1f}px")
        print(f"Exact match: {badge['height'] == flag['height']}")
        
        # Capture zoomed screenshot of that row
        meta_row = page.locator('.moto-q-meta-row')
        meta_row.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_meta_row_equal.png')
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_full_equal.png')
        
        browser.close()
    print('Done.')

if __name__ == '__main__':
    run()
