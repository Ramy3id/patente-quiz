import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    page.wait_for_load_state('networkidle')
    
    # Close any auth modal, close setup modal, enable guest or simulate saved plan
    page.evaluate("""() => {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('patente_theme_mode', 'light');
        
        // Remove all modal backdrops
        document.querySelectorAll('.sp-modal-backdrop, .auth-modal, [class*="modal"]').forEach(el => {
            el.classList.remove('open');
            el.style.display = 'none';
        });
        
        // Ensure plan is generated
        if (typeof generateDynamicTimeline === 'function') {
            generateDynamicTimeline();
        }
    }""")
    page.wait_for_timeout(400)
    
    # 1. Top of active plan page
    page.screenshot(path=f'{output_dir}\\piano_page_clean_top.png')
    
    # 2. Scroll 500px
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_page_clean_mid.png')

    # 3. Scroll to day card
    page.evaluate("""() => {
        const d = document.getElementById('activeDaySection');
        if (d) d.scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_page_clean_day.png')

    # 4. Scroll to timeline
    page.evaluate("""() => {
        const t = document.querySelector('.sp-timeline-section');
        if (t) t.scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_page_clean_timeline.png')

    browser.close()
    print("Clean page screenshots captured.")
