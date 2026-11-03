from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://localhost:8080/interactive_pages/scheda-esame.html')
        page.wait_for_timeout(1000)
        
        # Check which questions have an image
        q_data = page.evaluate('''() => {
            if (!window.exam || !window.exam.questions) return [];
            return window.exam.questions.map((q, idx) => ({
                idx: idx,
                id: q.id,
                immagine: q.immagine
            })).filter(x => x.immagine && x.immagine.trim() !== '');
        }''')
        print(f"Questions with image count: {len(q_data)}")
        
        if q_data:
            target_idx = q_data[0]['idx']
            img_src = q_data[0]['immagine']
            print(f"Navigating to question {target_idx + 1}, image: {img_src}")
            
            # Switch to moto mode
            page.click('#btnSkinMoto')
            page.wait_for_timeout(400)
            
            # Click that question in matrix
            page.click(f'.moto-cell:nth-child({target_idx + 1})')
            page.wait_for_timeout(600)
            
            img = page.locator('.moto-sign-img')
            panel = page.locator('.moto-sign-panel')
            print(f"Image visible: {img.is_visible()}")
            img_box = img.bounding_box()
            panel_box = panel.bounding_box()
            print(f"Image box: {img_box}")
            print(f"Panel box: {panel_box}")
            
            page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_with_actual_image.png')
            
            # Also check light mode with that image
            page.evaluate('() => document.documentElement.classList.add("light")')
            page.wait_for_timeout(500)
            page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_moto_light_with_image.png')
        
        browser.close()
    print('Image verification completed successfully.')

if __name__ == '__main__':
    run()
