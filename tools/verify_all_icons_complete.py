import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    page.wait_for_timeout(600)
    
    # Dismiss GDPR banner
    page.evaluate("""() => {
        localStorage.setItem('patente_gdpr_consent', 'accepted');
        const b = document.getElementById('patenteGdprBanner');
        if (b) b.remove();
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    }""")
    page.wait_for_timeout(300)
    
    # Scroll slightly to the Bento Tools and Capitolo 01 section (matching user screenshot)
    page.evaluate("() => { const el = document.querySelector('.bento-tools-section'); if(el) el.scrollIntoView(); }")
    page.wait_for_timeout(400)
    
    out_bento_dark = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\bento_and_cards_unified_dark.png'
    page.screenshot(path=out_bento_dark)
    print("Bento and cards dark screenshot saved.")

    # Light Mode
    page.evaluate("() => { document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light'); }")
    page.wait_for_timeout(300)
    out_bento_light = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\bento_and_cards_unified_light.png'
    page.screenshot(path=out_bento_light)
    print("Bento and cards light screenshot saved.")

    # Another page: interactive_pages/index.html to verify automatic hydration
    page.goto('http://localhost:8080/interactive_pages/index.html')
    page.wait_for_timeout(600)
    page.evaluate("""() => {
        const b = document.getElementById('patenteGdprBanner');
        if (b) b.remove();
    }""")
    out_interactive_page = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\interactive_pages_unified_icons.png'
    page.screenshot(path=out_interactive_page)
    print("Interactive pages verified.")

    browser.close()
