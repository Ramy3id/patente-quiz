import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Mobile Light (390 x 844)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    page.wait_for_load_state('networkidle')
    
    page.evaluate("""() => {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('patente_theme_mode', 'light');
        localStorage.setItem('patente_gdpr_accepted', 'true');
        
        const gdpr = document.querySelector('.gdpr-modal, [class*="gdpr"], [id*="gdpr"]');
        if (gdpr) gdpr.remove();

        openPlanSetupModal();
    }""")
    page.wait_for_timeout(400)
    
    # 1. Capture top view (Header pinned, full-width screen, hero card, Q1)
    page.screenshot(path=f'{output_dir}\\fullscreen_setup_top.png')
    
    # 2. Scroll modal down by 500px and capture
    page.evaluate("""() => {
        const modal = document.getElementById('planSetupModal');
        if (modal) modal.scrollTop = 500;
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\fullscreen_setup_mid.png')

    # 3. Scroll modal to bottom (Question 4 + Floating bottom action bar above bottom dock)
    page.evaluate("""() => {
        const modal = document.getElementById('planSetupModal');
        if (modal) modal.scrollTop = 1200;
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\fullscreen_setup_bottom.png')

    browser.close()
    print("All full-screen setup captures completed!")
