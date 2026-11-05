import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Mobile Light
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    page.wait_for_load_state('networkidle')
    
    page.evaluate("""() => {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('patente_theme_mode', 'light');
        localStorage.setItem('patente_gdpr_accepted', 'true');
        
        // Remove GDPR
        const gdpr = document.querySelector('.gdpr-modal, [class*="gdpr"], [id*="gdpr"]');
        if (gdpr) gdpr.remove();

        // Open Setup Modal
        openPlanSetupModal();
    }""")
    page.wait_for_timeout(400)
    
    # 1. Top of modal with safe gap below header & soft backdrop & Q1 & Q2
    page.screenshot(path=f'{output_dir}\\modal_refined_top.png')
    
    # 2. Scroll modal down to Q3 and Q4
    page.evaluate("""() => {
        const m = document.getElementById('planSetupModal');
        if (m) m.scrollTop = 450;
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\modal_refined_q3_q4.png')

    # 3. Test clicking sequential flow to verify interactive toggle
    page.evaluate("""() => {
        selectFlowMode('sequential');
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\modal_refined_sequential_clicked.png')

    browser.close()
    print("Recaptured modal refined screenshots successfully!")
