from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://localhost:8080/interactive_pages/scheda-esame.html')
        page.wait_for_timeout(1000)
        
        # 1. Inspect Switcher & Button bounding boxes in Modern Mode
        sw = page.locator('#masterSkinSwitcher').bounding_box()
        btn_m = page.locator('#btnSkinModern').bounding_box()
        btn_o = page.locator('#btnSkinMoto').bounding_box()
        pill1 = page.locator('.q-pill').first.bounding_box()
        
        print('=== SWITCHER GEOMETRY ===')
        print(f"Switcher capsule: top={sw['y']:.1f}, bottom={sw['y']+sw['height']:.1f}, height={sw['height']:.1f}px")
        print(f"Modern button: top={btn_m['y']:.1f}, bottom={btn_m['y']+btn_m['height']:.1f}, height={btn_m['height']:.1f}px")
        print(f"Moto button: top={btn_o['y']:.1f}, bottom={btn_o['y']+btn_o['height']:.1f}, height={btn_o['height']:.1f}px")
        print(f"Pill 1 top={pill1['y']:.1f}")
        gap = pill1['y'] - (sw['y'] + sw['height'])
        print(f"Gap from switcher bottom to Pill 1: {gap:.1f}px")
        
        # Check if button is inside switcher capsule:
        is_inside = (btn_m['y'] >= sw['y']) and (btn_m['y'] + btn_m['height'] <= sw['y'] + sw['height'] + 0.5)
        print(f"Modern button completely inside capsule: {is_inside}")
        
        # 2. Inspect Translation button vs Flag Review button
        flag = page.locator('#btnModernFlag').bounding_box()
        tr_btn = page.locator('#btnToggleTr').bounding_box()
        print('=== BUTTON HEIGHT COMPARISON ===')
        print(f"Flag review button height: {flag['height']:.1f}px")
        print(f"Translation button height: {tr_btn['height']:.1f}px")
        print(f"Exact height match: {flag['height'] == tr_btn['height']}")
        
        # Screenshot Modern Mode in Dark
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_modern_perfect_capsule.png')
        
        # Screenshot Modern Mode in Light
        page.evaluate('() => document.documentElement.classList.add("light")')
        page.wait_for_timeout(500)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_modern_light_perfect.png')
        
        # 3. Switch to Official Mode in Light Mode
        page.click('#btnSkinMoto')
        page.wait_for_timeout(500)
        
        moto_bg = page.evaluate('() => window.getComputedStyle(document.getElementById("motoScreenWrap")).backgroundColor')
        header_bg = page.evaluate('() => window.getComputedStyle(document.querySelector(".moto-top-header")).backgroundColor')
        text_color = page.evaluate('() => window.getComputedStyle(document.querySelector(".moto-text-italian")).color')
        
        print('=== OFFICIAL MODE LIGHT THEME ===')
        print(f"Terminal wrap bg: {moto_bg}")
        print(f"Header bg: {header_bg}")
        print(f"Question text color: {text_color}")
        
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_light_restored.png')
        
        # 4. Switch to Dark Mode in Official Mode
        page.evaluate('() => document.documentElement.classList.remove("light")')
        page.wait_for_timeout(500)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_dark_restored.png')
        
        browser.close()
    print('All tests completed successfully.')

if __name__ == '__main__':
    run()
