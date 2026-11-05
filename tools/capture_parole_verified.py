from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.goto('http://localhost:8080/Capitoli_Divisi/parole-quiz.html', wait_until='networkidle')
        page.wait_for_timeout(400)
        
        # 1. Capture Word Bank Buttons
        wb = page.locator('.chips-actions')
        if wb.count() > 0:
            wb.first.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\parole_word_bank_verified.png')
            print("Captured parole_word_bank_verified.png")
            
        # 2. Capture Filter Bar (VERO / FALSO)
        fb = page.locator('.segmented-filter-bar')
        if fb.count() > 0:
            fb.first.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\parole_filter_bar_verified.png')
            print("Captured parole_filter_bar_verified.png")
            
        # 3. Capture Semantic Families Shelf
        shelf = page.locator('#familiesShelf')
        if shelf.count() > 0:
            shelf.first.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\parole_shelf_verified.png')
            print("Captured parole_shelf_verified.png")
            
        browser.close()

if __name__ == '__main__':
    test()
