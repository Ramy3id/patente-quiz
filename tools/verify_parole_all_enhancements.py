import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:8080/Capitoli_Divisi/parole-quiz.html')
    page.wait_for_load_state('networkidle')

    # Remove any modal or gdpr overlay
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

    # 1. Populate words to see Word Bank and Actions centered
    page.click('.btn-action-preset:first-child')
    page.wait_for_timeout(400)

    # Scroll to word bank actions & chips
    page.evaluate("""() => {
        document.querySelector('.wordbank-deck').scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_wordbank_actions_centered.png')
    print("Captured verified_wordbank_actions_centered.png")

    # 2. Click on a semantic family pill to open Thesaurus card
    page.evaluate("""() => {
        const firstPill = document.querySelector('.family-pill');
        if (firstPill) firstPill.click();
    }""")
    page.wait_for_timeout(400)

    # Scroll to Thesaurus card (synonyms & traps)
    page.evaluate("""() => {
        document.getElementById('thesaurusCard').scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_thesaurus_clean_light.png')
    print("Captured verified_thesaurus_clean_light.png")

    # 3. Scroll to Search & Filter Controls: Segmented VERO/FALSO & Dropdown
    page.evaluate("""() => {
        document.querySelector('.search-filter-card').scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_filters_segmented_centered.png')
    print("Captured verified_filters_segmented_centered.png")

    # 4. Open Custom Dropdown and capture
    page.click('#pqDropdownBtn')
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_dropdown_open_bounded.png')
    print("Captured verified_dropdown_open_bounded.png")

    # 5. Switch to VERO and FALSO to verify interactions
    page.click('#btnAnsVero')
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_btn_vero_active.png')
    print("Captured verified_btn_vero_active.png")

    # 6. Dark Mode Check of Thesaurus
    page.evaluate("""() => {
        document.documentElement.classList.remove('light');
        document.documentElement.classList.add('dark');
        document.getElementById('thesaurusCard').scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\verified_thesaurus_dark.png')
    print("Captured verified_thesaurus_dark.png")

    browser.close()
    print("All verification steps completed!")
