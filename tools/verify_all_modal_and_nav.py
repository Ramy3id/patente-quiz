import sys
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 375, 'height': 812})
    page = context.new_page()
    page.goto('http://localhost:8080/interactive_pages/decodificatore-incroci.html')
    page.wait_for_load_state('networkidle')
    
    # 1. Force light mode & verify
    page.evaluate('window.applyTheme("light")')
    page.wait_for_timeout(300)
    
    # Verify nav arrows
    arrows = page.evaluate('''() => {
        const btns = document.querySelectorAll(".sim-nav-arrow-btn");
        return Array.from(btns).map(b => b.innerText.trim());
    }''')
    print('Nav arrow buttons text:', repr(arrows))
    
    # Verify simulation buttons under canvas
    sim_btns = page.evaluate('''() => {
        const row = document.querySelector(".sim-actions-row");
        const stageCol = document.querySelector(".sim-stage-col");
        const canvas = document.querySelector(".sim-canvas-wrap");
        const btns = row.querySelectorAll("button");
        return {
            rowParentIsStage: row.parentElement === stageCol,
            isDirectlyUnderCanvas: canvas.nextElementSibling === row,
            buttonCount: btns.length,
            buttonsText: Array.from(btns).map(b => b.innerText.trim()),
            buttonsTitle: Array.from(btns).map(b => b.getAttribute("title")),
            heights: Array.from(btns).map(b => window.getComputedStyle(b).height)
        };
    }''')
    print('Sim action buttons info:', repr(sim_btns))
    
    # Take screenshot of simulation canvas & 3 buttons in Light Mode
    sim_section = page.locator('#trafficSimSection')
    sim_section.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_sim_controls_light.png')
    
    # Open modal in Light Mode
    page.click('#btnOpenFigureModal')
    page.wait_for_timeout(400)
    
    # Check modal close button computed geometry
    close_geom = page.evaluate('''() => {
        const btn = document.querySelector(".fig-modal-close");
        const s = window.getComputedStyle(btn);
        const rect = btn.getBoundingClientRect();
        return {
            computedWidth: s.width,
            computedHeight: s.height,
            rectWidth: rect.width,
            rectHeight: rect.height,
            borderRadius: s.borderRadius,
            aspectRatio: s.aspectRatio,
            isPerfectCircle: Math.abs(rect.width - rect.height) < 1.0
        };
    }''')
    print('Close button geometry in Light Mode:', repr(close_geom))
    
    # Check modal colors in Light Mode
    modal_colors = page.evaluate('''() => {
        const card = document.querySelector(".fig-modal-card");
        const search = document.querySelector(".fig-modal-search");
        const title = document.querySelector(".fig-modal-title");
        return {
            cardBg: window.getComputedStyle(card).backgroundColor,
            searchBg: window.getComputedStyle(search).backgroundColor,
            searchColor: window.getComputedStyle(search).color,
            titleColor: window.getComputedStyle(title).color
        };
    }''')
    print('Modal colors in Light Mode:', repr(modal_colors))
    
    # Screenshot Light modal
    page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_fig_modal_light.png')
    
    # Close modal
    page.click('.fig-modal-close')
    page.wait_for_timeout(300)
    
    # 2. Switch to Dark Mode & test
    page.evaluate('window.applyTheme("dark")')
    page.wait_for_timeout(300)
    
    # Screenshot Dark simulation section
    sim_section.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_sim_controls_dark.png')
    
    # Open modal in Dark Mode
    page.click('#btnOpenFigureModal')
    page.wait_for_timeout(400)
    
    close_geom_dark = page.evaluate('''() => {
        const btn = document.querySelector(".fig-modal-close");
        const rect = btn.getBoundingClientRect();
        return {
            rectWidth: rect.width,
            rectHeight: rect.height,
            isPerfectCircle: Math.abs(rect.width - rect.height) < 1.0
        };
    }''')
    print('Close button geometry in Dark Mode:', repr(close_geom_dark))
    
    # Screenshot Dark modal
    page.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_fig_modal_dark.png')
    
    browser.close()
    print('Verification script completed successfully!')
