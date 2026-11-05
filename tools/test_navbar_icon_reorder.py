import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

CSS_TEST = """
@media (min-width: 993px) {
  #globalPortalNav {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    direction: rtl !important;
  }
  
  /* 1. Actions on EXTREME RIGHT (Order 1 in RTL) */
  #globalPortalNav .nav-desktop-actions {
    order: 1 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }

  /* 2. Tabs in CENTER (Order 2 in RTL) */
  #globalPortalNav .nav-desktop-tabs {
    order: 2 !important;
    margin: 0 auto !important;
  }

  /* 3. Logo and Chapters on EXTREME LEFT (Order 3 in RTL) */
  #globalPortalNav .nav-brand-group {
    order: 3 !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: row-reverse !important;
    align-items: center !important;
    gap: 10px !important;
  }

  /* Megamenu opens inwards to the right from left position */
  .nav-chapters-megamenu {
    left: 0 !important;
    right: auto !important;
  }

  /* Action Buttons -> Icon Only (38x38px) */
  .nav-desktop-actions .nav-search-trigger,
  .nav-desktop-actions .nav-progress-pill,
  .nav-desktop-actions .nav-auth-pill,
  .nav-desktop-actions .nav-theme-btn {
    width: 38px !important;
    min-width: 38px !important;
    max-width: 38px !important;
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    padding: 0 !important;
    border-radius: 10px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }

  .nav-desktop-actions .nav-search-trigger .search-text,
  .nav-desktop-actions .nav-search-trigger .search-kbd,
  .nav-desktop-actions .nav-progress-pill .prog-pill-label,
  .nav-desktop-actions .nav-progress-pill .prog-pill-val,
  .nav-desktop-actions .nav-progress-pill .prog-pill-bar-track,
  .nav-desktop-actions .nav-auth-pill span:not(:first-child),
  .nav-desktop-actions .nav-theme-btn .theme-label-span {
    display: none !important;
  }

  .nav-desktop-actions svg.ui-svg {
    width: 18px !important;
    height: 18px !important;
    margin: 0 !important;
  }
}
"""

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop 1440x900 (Light)
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'light');")

        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.evaluate("() => { document.documentElement.className = 'light'; }")
        page.add_style_tag(content=CSS_TEST)
        page.wait_for_timeout(400)

        # 1. Desktop Light View
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'reordered_nav_desktop_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 600})
        print("Captured reordered_nav_desktop_light.png")

        # 2. Megamenu open test
        page.evaluate("() => { const b = document.getElementById('btnToggleChaptersMenu'); if(b) b.click(); }")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'reordered_megamenu_open.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 720})
        print("Captured reordered_megamenu_open.png")

        # 3. Desktop Dark View
        page.evaluate("() => { const b = document.getElementById('btnToggleChaptersMenu'); if(b) b.click(); }") # close
        page.evaluate("() => { document.documentElement.className = 'dark'; }")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'reordered_nav_desktop_dark.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 600})
        print("Captured reordered_nav_desktop_dark.png")

        # 4. Mobile Check (390x844)
        context_mb = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, device_scale_factor=2)
        page_mb = context_mb.new_page()
        page_mb.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_mb.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_mb.add_style_tag(content=CSS_TEST)
        page_mb.wait_for_timeout(300)
        page_mb.screenshot(path=os.path.join(ARTIFACT_DIR, 'mobile_check_reorder_untouched.png'))
        print("Captured mobile_check_reorder_untouched.png")

        browser.close()

if __name__ == '__main__':
    test()
