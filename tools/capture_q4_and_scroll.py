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
        
        const gdpr = document.querySelector('.gdpr-modal, [class*="gdpr"], [id*="gdpr"]');
        if (gdpr) gdpr.remove();

        openPlanSetupModal();
    }""")
    page.wait_for_timeout(300)

    # Scroll directly to Question 4
    page.evaluate("""() => {
        const q4 = document.getElementById('optFlowCluster');
        if (q4) q4.scrollIntoView({ behavior: 'instant', block: 'center' });
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\q4_icon_cards.png')

    # Scroll all the way to bottom to check buttons and clearance
    page.evaluate("""() => {
        const modal = document.getElementById('planSetupModal');
        if (modal) modal.scrollTop = 3000;
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\bottom_clearance_verified.png')

    # Verify body scroll locking
    scroll_state = page.evaluate("""() => {
        return {
            bodyLocked: document.body.classList.contains('sp-modal-locked'),
            windowScrollY: window.scrollY,
            btnScrollTopDisplay: window.getComputedStyle(document.getElementById('patenteScrollTopBtn') || document.body).display
        };
    }""")
    print("Scroll state verification:", scroll_state)

    browser.close()
    print("Captures completed successfully!")
