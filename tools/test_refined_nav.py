import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

CSS_PATCH = """
@media (min-width: 993px) {
  /* 1. Equalize all tab heights in center */
  .nav-desktop-tabs .nav-dropdown-tab,
  .nav-desktop-tabs .nav-direct-tab {
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    border-radius: 10px !important;
    font-size: 0.86rem !important;
    font-weight: 700 !important;
    padding: 0 14px !important;
  }

  /* 2. Order of the 4 Actions from Right to Left:
     Order in RTL flexbox:
     1 (Far Right) = Auth 👤
     2 = Theme ☀️/🌙
     3 = Progress % 📊
     4 (Closest to Center) = Search 🔍
  */
  .nav-desktop-actions {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    direction: rtl !important;
  }

  .nav-desktop-actions .nav-auth-wrapper { order: 1 !important; }
  .nav-desktop-actions .nav-theme-btn { order: 2 !important; }
  .nav-desktop-actions .nav-progress-pill { order: 3 !important; }
  .nav-desktop-actions .nav-search-trigger { order: 4 !important; }

  /* 3. Remove all hover jumps / translateY */
  .nav-desktop-actions .nav-search-trigger,
  .nav-desktop-actions .nav-progress-pill,
  .nav-desktop-actions .nav-auth-pill,
  .nav-desktop-actions .nav-theme-btn,
  .nav-chapters-btn,
  .nav-dropdown-tab,
  .nav-direct-tab {
    transform: none !important;
    transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease !important;
  }
  .nav-desktop-actions .nav-search-trigger:hover,
  .nav-desktop-actions .nav-progress-pill:hover,
  .nav-desktop-actions .nav-auth-pill:hover,
  .nav-desktop-actions .nav-theme-btn:hover,
  .nav-chapters-btn:hover,
  .nav-dropdown-tab:hover,
  .nav-direct-tab:hover {
    transform: none !important;
  }

  /* 4. Luxury Circular Progress Button */
  .nav-progress-pill {
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
    text-decoration: none !important;
  }
}
"""

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'light');")

        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.add_style_tag(content=CSS_PATCH)

        # Inject Circular Progress Ring into #globalProgressPill & wrap auth
        page.evaluate("""() => {
            const authPill = document.getElementById('globalAuthPill');
            if (authPill && authPill.parentElement) {
                authPill.parentElement.className = 'nav-auth-wrapper';
            }

            const prog = document.getElementById('globalProgressPill');
            if (prog) {
                prog.innerHTML = `
                  <div class="prog-circular-wrap" style="position:relative; width:28px; height:28px; display:inline-flex; align-items:center; justify-content:center;">
                    <svg viewBox="0 0 36 36" style="width:28px; height:28px; transform:rotate(-90deg);">
                      <circle cx="18" cy="18" r="14" fill="none" stroke="currentColor" stroke-width="3" opacity="0.15"></circle>
                      <circle cx="18" cy="18" r="14" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="88" stroke-dashoffset="88" stroke-linecap="round"></circle>
                    </svg>
                    <span style="position:absolute; font-size:10px; font-weight:800; font-family:sans-serif; color:inherit; direction:ltr;">0%</span>
                  </div>
                `;
            }
        }""")
        page.wait_for_timeout(400)

        # Check tab heights
        tabs = page.evaluate("""() => {
            const res = [];
            document.querySelectorAll('.nav-desktop-tabs > *').forEach((el) => {
                const btn = el.querySelector('.nav-dropdown-tab') || el;
                res.push({
                    name: btn.innerText.trim().replace(/\\n/g, ' '),
                    height: btn.getBoundingClientRect().height
                });
            });
            return res;
        }""")
        print("Tab Heights after fix:", tabs)

        # Check Action icons order from right to left
        actions_order = page.evaluate("""() => {
            const actions = document.querySelectorAll('.nav-desktop-actions > *');
            const list = [];
            actions.forEach(el => {
                const r = el.getBoundingClientRect();
                list.push({
                    id: el.id || el.className,
                    right: r.right,
                    left: r.left
                });
            });
            list.sort((a, b) => b.right - a.right); // Sort from Rightmost to Leftmost
            return list;
        }""")
        print("Actions Order (Rightmost to Leftmost):\n", actions_order)

        # Screenshot top view
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_refined_order_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured nav_refined_order_light.png")

        browser.close()

if __name__ == '__main__':
    test()
