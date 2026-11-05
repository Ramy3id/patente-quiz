import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

CSS_TEST = """
@media (min-width: 993px) {
  #globalPortalNav,
  .unified-portal-nav {
    max-width: 1200px !important;
    width: calc(100% - 36px) !important;
    margin: 12px auto 0 auto !important;
    top: 12px !important;
    border-radius: 16px !important;
    padding: 0 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
    background: rgba(15, 23, 42, 0.88) !important;
  }

  html.light #globalPortalNav,
  html.light .unified-portal-nav {
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.04) !important;
    background: rgba(255, 255, 255, 0.92) !important;
  }
}
"""

def test_implementation():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # 1. Desktop Test (Light Mode, 1440x900)
        context_dt = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page_dt = context_dt.new_page()
        page_dt.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_dt.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_dt.evaluate("() => { document.documentElement.className = 'light'; }")
        page_dt.add_style_tag(content=CSS_TEST)
        page_dt.wait_for_timeout(300)
        
        # Capture Top view
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'floating_desktop_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 600})
        
        # Test scroll (to verify sticky floating behavior)
        page_dt.evaluate("() => window.scrollTo(0, 450)")
        page_dt.wait_for_timeout(300)
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'floating_desktop_scrolled.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 600})

        # Test Megamenu Open in floating mode
        page_dt.evaluate("() => window.scrollTo(0, 0)")
        page_dt.evaluate("() => { const b = document.getElementById('btnToggleChaptersMenu'); if(b) b.click(); }")
        page_dt.wait_for_timeout(300)
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'floating_megamenu_open.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 700})

        # 2. Desktop Test (Dark Mode, 1440x900)
        page_dt.evaluate("() => { document.documentElement.className = 'dark'; }")
        page_dt.evaluate("() => { const b = document.getElementById('btnToggleChaptersMenu'); if(b) b.click(); }") # close menu
        page_dt.wait_for_timeout(300)
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'floating_desktop_dark.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 600})

        # 3. Mobile Test (Pixel 5: 393x851)
        context_mb = browser.new_context(viewport={"width": 393, "height": 851}, is_mobile=True, device_scale_factor=2)
        page_mb = context_mb.new_page()
        page_mb.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_mb.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_mb.evaluate("() => { document.documentElement.className = 'light'; }")
        page_mb.add_style_tag(content=CSS_TEST)
        page_mb.wait_for_timeout(300)
        page_mb.screenshot(path=os.path.join(ARTIFACT_DIR, 'mobile_check_floating_untouched.png'))

        browser.close()
        print("All tests completed successfully!")

if __name__ == '__main__':
    test_implementation()
