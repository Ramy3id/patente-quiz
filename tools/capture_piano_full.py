import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    page.wait_for_load_state('networkidle')
    
    page.evaluate("""() => {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('patente_theme_mode', 'light');
        localStorage.setItem('patente_gdpr_accepted', 'true');
        
        // Remove GDPR banner completely
        const gdpr = document.querySelector('.gdpr-modal, [class*="gdpr"], [id*="gdpr"]');
        if (gdpr) gdpr.remove();
        document.querySelectorAll('.modal-backdrop, .fixed').forEach(el => {
            if (el.textContent.includes('GDPR') || el.textContent.includes('الخصوصية')) el.remove();
        });

        // Close all modals
        document.querySelectorAll('.sp-modal-backdrop, .auth-modal').forEach(el => {
            el.classList.remove('open');
            el.style.display = 'none';
        });

        // Make sure timeline is rendered
        if (typeof generateDynamicTimeline === 'function') generateDynamicTimeline();
    }""")
    page.wait_for_timeout(400)
    
    # 1. Hero and quick modes
    page.screenshot(path=f'{output_dir}\\piano_full_1_hero.png')
    
    # 2. Scroll to active day
    page.evaluate("window.scrollTo(0, 650)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_full_2_activeday.png')

    # 3. Scroll to timeline grid
    page.evaluate("window.scrollTo(0, 1300)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_full_3_timeline.png')

    browser.close()
    print("Full view screenshots saved.")
