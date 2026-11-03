import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://localhost:8080/interactive_pages/decodificatore-incroci.html')
    page.wait_for_load_state('networkidle')
    
    # Temporarily set the innerHTML of both buttons to test
    page.evaluate('''() => {
        const wrap = document.querySelector(".sim-arrows-wrap");
        const prevBtn = wrap.querySelectorAll("button")[0];
        const nextBtn = wrap.querySelectorAll("button")[1];
        
        prevBtn.innerHTML = '<span class="nav-arrow-icon">▶</span><span>السابق</span>';
        nextBtn.innerHTML = '<span>التالي</span><span class="nav-arrow-icon">◀</span>';
    }''')
    
    pos = page.evaluate('''() => {
        const wrap = document.querySelector(".sim-arrows-wrap");
        const prevBtn = wrap.querySelectorAll("button")[0];
        const nextBtn = wrap.querySelectorAll("button")[1];
        
        const prevArrow = prevBtn.querySelector(".nav-arrow-icon").getBoundingClientRect();
        const prevText = prevBtn.querySelector("span:not(.nav-arrow-icon)").getBoundingClientRect();
        
        const nextArrow = nextBtn.querySelector(".nav-arrow-icon").getBoundingClientRect();
        const nextText = nextBtn.querySelector("span:not(.nav-arrow-icon)").getBoundingClientRect();
        
        return {
            prevArrowX: prevArrow.x,
            prevTextX: prevText.x,
            isPrevArrowBeforeInRTL: prevArrow.x > prevText.x, // In RTL, "before" means further to the right (larger X)
            nextArrowX: nextArrow.x,
            nextTextX: nextText.x,
            isNextArrowAfterInRTL: nextArrow.x < nextText.x  // In RTL, "after" means further to the left (smaller X)
        };
    }''')
    print('Position check:', pos)
    
    # Screenshot the nav header
    page.locator('.sim-nav-header').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\test_nav_header_arrows.png')
    browser.close()
