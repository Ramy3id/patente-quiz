import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://localhost:8080/interactive_pages/scheda-esame.html')
        page.wait_for_timeout(1000)
        
        # 1. Check Modern Mode
        hub = page.locator('#examMasterControlHub').bounding_box()
        switcher = page.locator('#masterSkinSwitcher').bounding_box()
        pill1 = page.locator('.q-pill').first.bounding_box()
        
        print('=== MODERN MODE ===')
        print(f"Hub bottom: {hub['y'] + hub['height']}")
        print(f"Switcher bottom: {switcher['y'] + switcher['height']}")
        print(f"Pill 1 top: {pill1['y']}")
        gap = pill1['y'] - (switcher['y'] + switcher['height'])
        print(f"Gap between switcher and Pill 1: {gap:.1f}px")
        
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_modern_gap_fixed.png')
        
        # 2. Switch to Official Mode
        page.click('#btnSkinMoto')
        page.wait_for_timeout(500)
        
        moto_wrap = page.locator('#motoScreenWrap').bounding_box()
        print('=== OFFICIAL MODE (Q1) ===')
        print(f"Hub bottom: {hub['y'] + hub['height']}")
        print(f"Moto wrap top: {moto_wrap['y']}")
        moto_gap = moto_wrap['y'] - (hub['y'] + hub['height'])
        print(f"Gap between hub and moto wrap: {moto_gap:.1f}px")
        
        btn_v = page.locator('.btn-moto-touch.v').bounding_box()
        btn_f = page.locator('.btn-moto-touch.f').bounding_box()
        print(f"Btn V box: {btn_v}")
        print(f"Btn F box: {btn_f}")
        
        btn_v_color = page.evaluate('() => window.getComputedStyle(document.querySelector(".btn-moto-touch.v")).backgroundColor')
        print(f"Btn V background: {btn_v_color}")
        
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_q1_fixed.png')
        
        # 3. Check Question 2 in Official Mode (Intersection image)
        page.click('.moto-cell:nth-child(2)')
        page.wait_for_timeout(500)
        
        img = page.locator('.moto-sign-img')
        print('=== OFFICIAL MODE (Q2 with Image) ===')
        print(f"Img visible: {img.is_visible()}")
        img_box = img.bounding_box()
        print(f"Img bounding box: {img_box}")
        
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_q2_image_fixed.png')
        
        # 4. Check Light Mode in Official Mode
        page.evaluate('() => document.documentElement.classList.add("light")')
        page.wait_for_timeout(500)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_light_q2_fixed.png')
        
        # 5. Switch back to Modern in Light Mode
        page.click('#btnSkinModern')
        page.wait_for_timeout(500)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_modern_light_fixed.png')
        
        browser.close()
    print('All verifications completed successfully.')

if __name__ == '__main__':
    run()
