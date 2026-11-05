import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Mobile Light
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    page.wait_for_load_state('networkidle')
    page.evaluate("""() => {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('patente_theme_mode', 'light');
        const gdpr = document.getElementById('gdprConsentModal') || document.querySelector('.gdpr-card') || document.querySelector('[class*="gdpr"]');
        if (gdpr) gdpr.style.display = 'none';
        const modalBackdrops = document.querySelectorAll('.modal-backdrop, .fixed');
        modalBackdrops.forEach(el => {
            if (el.textContent.includes('GDPR') || el.textContent.includes('الخصوصية')) el.style.display = 'none';
        });
    }""")
    page.wait_for_timeout(400)
    
    # Screenshot top
    page.screenshot(path=f'{output_dir}\\piano_studio_mobile_top.png')
    
    # Scroll down 600px
    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_studio_mobile_mid.png')

    # Scroll down 1200px
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_studio_mobile_bottom.png')

    # 2. Desktop Light
    desk_page = browser.new_page(viewport={'width': 1200, 'height': 900})
    desk_page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    desk_page.wait_for_load_state('networkidle')
    desk_page.evaluate("""() => {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('patente_theme_mode', 'light');
        const gdpr = document.getElementById('gdprConsentModal') || document.querySelector('.gdpr-card') || document.querySelector('[class*="gdpr"]');
        if (gdpr) gdpr.style.display = 'none';
    }""")
    desk_page.wait_for_timeout(400)
    desk_page.screenshot(path=f'{output_dir}\\piano_studio_desktop_top.png')

    browser.close()
    print("Screenshots taken successfully.")
