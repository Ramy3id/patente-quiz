import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop 1440x900 (Light Mode)
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'light');")

        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.wait_for_timeout(600)

        # 1. Alignment check with Hero
        info = page.evaluate("""() => {
            const nav = document.getElementById('globalPortalNav').getBoundingClientRect();
            const hero = document.querySelector('.ch-portal-header').getBoundingClientRect();
            const auth = document.getElementById('globalAuthPill');
            const search = document.getElementById('btnOpenGlobalSearch');
            const prog = document.getElementById('globalProgressPill');
            const theme = document.querySelector('.nav-theme-btn');
            const chap = document.getElementById('btnToggleChaptersMenu');

            return {
                nav: {left: nav.left, right: nav.right, width: nav.width, height: nav.height, top: nav.top},
                hero: {left: hero.left, right: hero.right, width: hero.width, top: hero.top},
                diff_left: nav.left - hero.left,
                diff_right: nav.right - hero.right,
                buttons: {
                    search_w: search ? search.getBoundingClientRect().width : 0,
                    prog_w: prog ? prog.getBoundingClientRect().width : 0,
                    auth_w: auth ? auth.getBoundingClientRect().width : 0,
                    auth_text: auth ? auth.innerText.trim() : '',
                    theme_w: theme ? theme.getBoundingClientRect().width : 0,
                    chap_text: chap ? chap.innerText.trim() : ''
                }
            };
        }""")
        print("Alignment & Buttons Inspection:\n", info)

        # Screenshot 1: Top View
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_fixed_top_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured nav_fixed_top_light.png")

        # Screenshot 2: Scrolled View (450px down) to verify fixed behavior
        page.evaluate("() => window.scrollTo(0, 450)")
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_fixed_scrolled_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured nav_fixed_scrolled_light.png")

        # Screenshot 3: Dark Mode
        page.evaluate("() => window.scrollTo(0, 0)")
        page.evaluate("() => { document.documentElement.className = 'dark'; localStorage.setItem('patente_theme', 'dark'); }")
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_fixed_top_dark.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured nav_fixed_top_dark.png")

        # Screenshot 4: Mobile View (390x844)
        context_mb = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, device_scale_factor=2)
        page_mb = context_mb.new_page()
        page_mb.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_mb.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_mb.wait_for_timeout(400)
        page_mb.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_mobile_still_perfect.png'))
        print("Captured nav_mobile_still_perfect.png")

        browser.close()

if __name__ == '__main__':
    test()
