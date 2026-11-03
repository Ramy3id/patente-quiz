import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    desktop_page = browser.new_page(viewport={'width': 1200, 'height': 800})
    desktop_page.goto('http://127.0.0.1:8080/Capitoli_Divisi/parole-quiz.html')
    desktop_page.wait_for_load_state('networkidle')
    desktop_page.evaluate("""() => {
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
    desktop_page.wait_for_timeout(300)
    desktop_page.screenshot(path=f'{output_dir}\\parole_quiz_desktop_final.png')
    print('Desktop screenshot saved.')
    browser.close()
