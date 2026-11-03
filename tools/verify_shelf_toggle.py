import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:8080/Capitoli_Divisi/parole-quiz.html')
    page.wait_for_load_state('networkidle')

    # Remove modals / gdpr
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
    page.wait_for_timeout(300)

    # Scroll to families shelf
    page.evaluate("""() => {
        const shelf = document.getElementById('familiesShelf');
        if (shelf) shelf.scrollIntoView({ behavior: 'instant', block: 'start' });
    }""")
    page.wait_for_timeout(300)

    # 1. Capture collapsed view (only 6 families visible + toggle button)
    page.screenshot(path=f'{output_dir}\\verified_shelf_collapsed_6.png')
    print("Captured verified_shelf_collapsed_6.png")

    # 2. Click toggle button to expand
    page.click('#btnToggleFamilies')
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_shelf_expanded_all.png')
    print("Captured verified_shelf_expanded_all.png")

    # 3. Click toggle button again to collapse
    page.click('#btnToggleFamilies')
    page.wait_for_timeout(300)

    browser.close()
    print("Verification completed successfully.")
