import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'light');")

        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.wait_for_timeout(600)

        # Inspection
        info = page.evaluate("""() => {
            const nav = document.getElementById('globalPortalNav').getBoundingClientRect();
            const hero = document.querySelector('.ch-portal-header').getBoundingClientRect();

            // Tabs in center
            const tabs = [];
            document.querySelectorAll('.nav-desktop-tabs > *').forEach(el => {
                const btn = el.querySelector('.nav-dropdown-tab') || el;
                tabs.push({
                    name: btn.innerText.trim().replace(/\\n/g, ' '),
                    height: btn.getBoundingClientRect().height,
                    border: getComputedStyle(btn).border
                });
            });

            // Actions on right (from rightmost to leftmost)
            const actions = [];
            document.querySelectorAll('.nav-desktop-actions > *').forEach(el => {
                const r = el.getBoundingClientRect();
                actions.push({
                    id: el.id || el.className,
                    right: r.right,
                    left: r.left,
                    width: r.width,
                    height: r.height,
                    text: el.innerText.trim().replace(/\\n/g, ' ')
                });
            });
            actions.sort((a, b) => b.right - a.right);

            return {
                alignment: {
                    nav_left: nav.left,
                    hero_left: hero.left,
                    nav_right: nav.right,
                    hero_right: hero.right,
                    nav_width: nav.width,
                    hero_width: hero.width,
                    diff_left: nav.left - hero.left,
                    diff_right: nav.right - hero.right
                },
                tabs: tabs,
                actions_order: actions
            };
        }""")

        print("Full UI Architecture Verification:")
        import json
        print(json.dumps(info, indent=2, ensure_ascii=False))

        # Screenshots
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'perfect_nav_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured perfect_nav_light.png")

        # Scrolled view (450px)
        page.evaluate("() => window.scrollTo(0, 450)")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'perfect_nav_scrolled.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured perfect_nav_scrolled.png")

        # Dark mode
        page.evaluate("() => window.scrollTo(0, 0)")
        page.evaluate("() => { document.documentElement.className = 'dark'; localStorage.setItem('patente_theme', 'dark'); }")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'perfect_nav_dark.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured perfect_nav_dark.png")

        browser.close()

if __name__ == '__main__':
    verify()
