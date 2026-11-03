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

    # 1. Capture Word Bank Buttons (no background behind them)
    page.click('.btn-action-preset:first-child')
    page.wait_for_timeout(300)
    page.evaluate("""() => {
        const deck = document.querySelector('.wordbank-deck');
        if (deck) deck.scrollIntoView({ behavior: 'instant', block: 'start' });
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_wordbank_no_bg.png')
    print("Captured verified_wordbank_no_bg.png")

    # 2. Capture Families Shelf (no horizontal scroll, wrapped nicely)
    page.evaluate("""() => {
        const shelf = document.getElementById('familiesShelf');
        if (shelf) shelf.scrollIntoView({ behavior: 'instant', block: 'start' });
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_shelf_no_scroll.png')
    print("Captured verified_shelf_no_scroll.png")

    # 3. Capture Filter Buttons (الكل / VERO / FALSO with no background behind them)
    page.evaluate("""() => {
        const filterBar = document.querySelector('.segmented-filter-bar');
        if (filterBar) filterBar.scrollIntoView({ behavior: 'instant', block: 'center' });
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_filters_no_bg.png')
    print("Captured verified_filters_no_bg.png")

    browser.close()
    print("All captures completed successfully.")
