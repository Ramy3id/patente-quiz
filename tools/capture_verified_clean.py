import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Mobile Dark Mode
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    page.goto('http://localhost:8080/index.html')
    page.wait_for_timeout(500)
    
    # Dismiss GDPR banner
    page.evaluate("""() => {
        localStorage.setItem('patente_gdpr_consent', 'accepted');
        const b = document.getElementById('patenteGdprBanner');
        if (b) b.remove();
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    }""")
    page.wait_for_timeout(400)
    
    # Screenshot of homepage with floating hybrid dock in view
    out_mobile_dock = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\mobile_dock_verified_clean.png'
    page.screenshot(path=out_mobile_dock)
    print("Mobile dark dock saved.")
    
    # Scroll to footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(400)
    out_mobile_footer = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\mobile_footer_verified_clean.png'
    page.screenshot(path=out_mobile_footer)
    print("Mobile dark footer saved.")

    # 2. Mobile Light Mode
    page.evaluate("() => { document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light'); }")
    page.wait_for_timeout(300)
    out_mobile_footer_light = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\mobile_footer_verified_clean_light.png'
    page.screenshot(path=out_mobile_footer_light)
    print("Mobile light footer saved.")

    # Scroll up in light mode to see dock on page
    page.evaluate("() => window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    out_mobile_dock_light = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\mobile_dock_verified_clean_light.png'
    page.screenshot(path=out_mobile_dock_light)
    print("Mobile light dock saved.")

    # 3. Desktop View (1280x900)
    page_d = browser.new_page(viewport={'width': 1280, 'height': 900})
    page_d.goto('http://localhost:8080/index.html')
    page_d.wait_for_timeout(500)
    page_d.evaluate("""() => {
        localStorage.setItem('patente_gdpr_consent', 'accepted');
        const b = document.getElementById('patenteGdprBanner');
        if (b) b.remove();
        window.scrollTo(0, document.body.scrollHeight);
    }""")
    page_d.wait_for_timeout(400)
    out_desktop_footer = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\desktop_footer_verified_clean.png'
    page_d.screenshot(path=out_desktop_footer)
    print("Desktop footer saved.")

    browser.close()
