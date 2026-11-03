from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://localhost:8080/interactive_pages/parole-spia.html')
        page.wait_for_timeout(1000)
        
        # 1. Dark Mode Verification
        doc_w = page.evaluate('() => document.documentElement.scrollWidth')
        win_w = page.evaluate('() => window.innerWidth')
        print(f"Viewport: winWidth={win_w}, docScrollWidth={doc_w}, hasHorizontalScroll={doc_w > win_w}")
        
        stats_strip = page.locator('.ps-stats-strip').bounding_box()
        items = page.locator('.ps-stat-item')
        print(f"Stats strip: {stats_strip}")
        print(f"Stat items count: {items.count()}")
        for i in range(items.count()):
            box = items.nth(i).bounding_box()
            print(f"  Item {i+1} box: {box}")
        
        # Check filters
        filters_row = page.locator('.ps-filters-row').first.bounding_box()
        btns = page.locator('.ps-controls').first.locator('.ps-filter-btn')
        print(f"Filters row: {filters_row}")
        print(f"Buttons count: {btns.count()}")
        for i in range(btns.count()):
            b_box = btns.nth(i).bounding_box()
            print(f"  Btn {i+1} box: x={b_box['x']:.1f}, y={b_box['y']:.1f}, w={b_box['width']:.1f}, h={b_box['height']:.1f}")
        
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_radar_dark_redesign.png')
        
        # 2. Light Mode Verification
        page.evaluate('() => document.documentElement.classList.add("light")')
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_radar_light_redesign.png')
        
        # Zoomed screenshot of Hero card
        page.locator('.ps-hero').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_radar_hero_strip_zoom.png')
        
        # Zoomed screenshot of Controls card
        page.locator('.ps-controls').first.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_radar_filters_card_zoom.png')
        
        # 3. Test Tab 2 (Sign Traps)
        page.click('#tabBtnSigns')
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_radar_tab2_signs.png')
        
        # 4. Test Tab 3 (Theory Rules)
        page.click('#tabBtnTheory')
        page.wait_for_timeout(400)
        page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_radar_tab3_theory.png')
        
        browser.close()
    print('All Playwright tests completed successfully.')

if __name__ == '__main__':
    run()
