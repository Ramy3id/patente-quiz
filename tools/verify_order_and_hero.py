import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 375, 'height': 812})
    page = context.new_page()
    page.goto('http://localhost:8080/interactive_pages/decodificatore-incroci.html')
    page.wait_for_load_state('networkidle')
    
    # 1. Light mode check
    page.evaluate('window.applyTheme("light")')
    page.wait_for_timeout(300)
    
    # Check stats strip
    stats_data = page.evaluate('''() => {
        const items = document.querySelectorAll(".inc-stat-item");
        return Array.from(items).map(item => {
            const s = window.getComputedStyle(item);
            return {
                text: item.innerText.trim(),
                bg: s.backgroundColor,
                color: s.color,
                border: s.borderColor
            };
        });
    }''')
    print('Stats strip data in Light mode:', stats_data)
    
    # Screenshot hero section
    page.locator('.inc-hero').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_hero_stats_strip_light.png')
    
    # Check order card for figure 608
    order_data_608 = page.evaluate('''() => {
        const card = document.getElementById("simOrderCard");
        const flow = card.querySelector(".sim-order-flow-track").innerText.trim();
        const steps = Array.from(card.querySelectorAll(".sim-order-step-item")).map(s => s.innerText.trim().replace(/\\n/g, ' '));
        return { flow, steps };
    }''')
    print('Figure 608 order data:', order_data_608)
    
    # Screenshot order card for 608
    page.locator('.sim-status-box').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_order_card_608_light.png')
    
    # Test Figure 637 (which has contemporaneamente C + A)
    page.evaluate('loadSimIncrocio("637")')
    page.wait_for_timeout(300)
    order_data_637 = page.evaluate('''() => {
        const card = document.getElementById("simOrderCard");
        const flow = card.querySelector(".sim-order-flow-track").innerText.trim();
        const steps = Array.from(card.querySelectorAll(".sim-order-step-item")).map(s => s.innerText.trim().replace(/\\n/g, ' '));
        return { flow, steps };
    }''')
    print('Figure 637 order data (contemporaneamente):', order_data_637)
    page.locator('.sim-status-box').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_order_card_637_light.png')
    
    # 2. Dark mode check
    page.evaluate('window.applyTheme("dark")')
    page.evaluate('loadSimIncrocio("608")')
    page.wait_for_timeout(300)
    
    page.locator('.inc-hero').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_hero_stats_strip_dark.png')
    page.locator('.sim-status-box').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_order_card_608_dark.png')
    
    browser.close()
    print('All checks completed successfully!')
