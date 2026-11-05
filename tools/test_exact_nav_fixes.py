import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

CSS_PATCH = """
@media (min-width: 993px) {
  body {
    padding-top: 88px !important;
  }

  #globalPortalNav,
  .unified-portal-nav {
    position: fixed !important;
    top: 14px !important;
    left: calc((100% - 1164px) / 2) !important;
    right: calc((100% - 1164px) / 2) !important;
    margin: 0 !important;
    width: 1164px !important;
    max-width: 1164px !important;
    height: 64px !important;
    min-height: 64px !important;
    max-height: 64px !important;
    border-radius: 18px !important;
    padding: 0 16px !important;
    margin: 0 !important;
    z-index: 10000 !important;
    box-sizing: border-box !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    direction: rtl !important;
    background: rgba(15, 23, 42, 0.88) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
  }

  html.light #globalPortalNav,
  html.light .unified-portal-nav {
    background: rgba(255, 255, 255, 0.94) !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08), 0 2px 8px rgba(15, 23, 42, 0.04) !important;
  }

  /* 1. Actions on FAR RIGHT */
  #globalPortalNav .nav-desktop-actions {
    order: 1 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    flex-shrink: 0 !important;
  }

  /* 2. Tabs in CENTER */
  #globalPortalNav .nav-desktop-tabs {
    order: 2 !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
  }

  /* 3. Logo and Chapters on FAR LEFT */
  #globalPortalNav .nav-brand-group {
    order: 3 !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: row-reverse !important;
    align-items: center !important;
    gap: 8px !important;
    flex-shrink: 0 !important;
  }

  /* Chapters button compact */
  .nav-chapters-btn {
    height: 40px !important;
    padding: 0 10px !important;
    gap: 5px !important;
    font-size: 0.82rem !important;
    border-radius: 10px !important;
  }
  .nav-chapters-btn .btn-label {
    font-weight: 700 !important;
  }

  /* Action Buttons -> Strictly 40x40 Icon Only */
  .nav-desktop-actions .nav-search-trigger,
  .nav-desktop-actions .nav-progress-pill,
  .nav-desktop-actions .nav-auth-pill,
  .nav-desktop-actions .nav-theme-btn {
    width: 40px !important;
    min-width: 40px !important;
    max-width: 40px !important;
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    padding: 0 !important;
    border-radius: 10px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    cursor: pointer !important;
    overflow: hidden !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #94a3b8 !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }

  html.light .nav-desktop-actions .nav-search-trigger,
  html.light .nav-desktop-actions .nav-progress-pill,
  html.light .nav-desktop-actions .nav-auth-pill,
  html.light .nav-desktop-actions .nav-theme-btn {
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.1) !important;
    color: #475569 !important;
  }

  /* Hide any text spans that might be injected into auth or progress */
  .nav-desktop-actions .nav-search-trigger .search-text,
  .nav-desktop-actions .nav-search-trigger .search-kbd,
  .nav-desktop-actions .nav-progress-pill .prog-pill-label,
  .nav-desktop-actions .nav-progress-pill .prog-pill-val,
  .nav-desktop-actions .nav-progress-pill .prog-pill-bar-track,
  .nav-desktop-actions .nav-auth-pill span:not(.auth-icon-wrap):not(:first-child),
  .nav-desktop-actions .nav-theme-btn .theme-label-span {
    display: none !important;
  }

  .nav-desktop-actions svg.ui-svg {
    width: 19px !important;
    height: 19px !important;
    stroke-width: 2 !important;
    margin: 0 !important;
  }
}
"""

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'light');")

        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.evaluate("() => { document.documentElement.className = 'light'; }")
        page.add_style_tag(content=CSS_PATCH)

        # Make chapters button compact
        page.evaluate("""() => {
            const btn = document.getElementById('btnToggleChaptersMenu');
            if (btn) {
                const label = btn.querySelector('.btn-label');
                if (label) label.textContent = '1-25';
            }
            // Ensure auth pill only has icon
            const auth = document.getElementById('globalAuthPill');
            if (auth) {
                auth.innerHTML = '<span class="auth-icon-wrap" style="display:inline-flex;align-items:center;justify-content:center;"><svg class="ui-svg" viewBox="0 0 24 24" style="width:19px;height:19px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></span>';
            }
        }""")
        page.wait_for_timeout(400)

        # 1. Check coordinates alignment with hero
        info = page.evaluate("""() => {
            const nav = document.getElementById('globalPortalNav').getBoundingClientRect();
            const hero = document.querySelector('.ch-portal-header').getBoundingClientRect();
            return {
                nav: {left: nav.left, right: nav.right, width: nav.width, height: nav.height},
                hero: {left: hero.left, right: hero.right, width: hero.width}
            };
        }""")
        print("Alignment comparison:", info)

        # Screenshot top view
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'fixed_perfect_nav_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})

        # Screenshot scrolled view (to verify fixed position!)
        page.evaluate("() => window.scrollTo(0, 450)")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'fixed_perfect_nav_scrolled.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})

        browser.close()

if __name__ == '__main__':
    run()
