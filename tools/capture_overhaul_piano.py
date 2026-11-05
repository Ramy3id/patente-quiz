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
        localStorage.setItem('patente_gdpr_accepted', 'true');
        
        // Remove GDPR
        const gdpr = document.querySelector('.gdpr-modal, [class*="gdpr"], [id*="gdpr"]');
        if (gdpr) gdpr.remove();
        document.querySelectorAll('.modal-backdrop, .fixed').forEach(el => {
            if (el.textContent.includes('GDPR') || el.textContent.includes('الخصوصية')) el.remove();
        });

        // Close modal initially
        const m = document.getElementById('planSetupModal');
        if (m) m.classList.remove('open');

        if (typeof generateDynamicTimeline === 'function') generateDynamicTimeline();
    }""")
    page.wait_for_timeout(400)
    
    # Capture 1: Hero & 2x2 metrics
    page.screenshot(path=f'{output_dir}\\piano_overhaul_mobile_hero.png')
    
    # Capture 2: Readiness card
    page.evaluate("window.scrollTo(0, 680)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_overhaul_mobile_readiness.png')

    # Capture 3: Mission stations
    page.evaluate("""() => {
        const m = document.getElementById('missionCardSection');
        if (m) m.scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_overhaul_mobile_mission.png')

    # Capture 4: Timeline & pills
    page.evaluate("""() => {
        const t = document.querySelector('.sp-timeline-section');
        if (t) t.scrollIntoView();
    }""")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\piano_overhaul_mobile_timeline.png')

    # Capture 5: Modal Setup open
    page.evaluate("""() => {
        const m = document.getElementById('planSetupModal');
        if (m) {
            m.style.display = 'flex';
            m.classList.add('open');
        }
    }""")
    page.wait_for_timeout(400)
    page.screenshot(path=f'{output_dir}\\piano_overhaul_modal_open.png')

    # 2. Desktop Light View
    desk = browser.new_page(viewport={'width': 1200, 'height': 850})
    desk.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    desk.wait_for_load_state('networkidle')
    desk.evaluate("""() => {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('patente_theme_mode', 'light');
        localStorage.setItem('patente_gdpr_accepted', 'true');
        const gdpr = document.querySelector('.gdpr-modal, [class*="gdpr"], [id*="gdpr"]');
        if (gdpr) gdpr.remove();
        const m = document.getElementById('planSetupModal');
        if (m) m.classList.remove('open');
        if (typeof generateDynamicTimeline === 'function') generateDynamicTimeline();
    }""")
    desk.wait_for_timeout(400)
    desk.screenshot(path=f'{output_dir}\\piano_overhaul_desktop_hero.png')

    browser.close()
    print("Recaptured all overhaul screenshots successfully!")
