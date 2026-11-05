import re

CSS_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css"
JS_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js"

# 1. Update theme-modes.css
with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css_content = f.read()

desktop_floating_css = """
/* ==========================================================================
   DESKTOP FLOATING ISLAND CAPSULE SPECIFICATION (Apple VisionOS / Raycast)
   Preserves mobile edge-to-edge 100% while floating on 1200px desktop grid
   ========================================================================== */
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

marker = "/* Master Baseline Content Spacing Below Frozen Header */"
if marker in css_content and "DESKTOP FLOATING ISLAND CAPSULE SPECIFICATION" not in css_content:
    css_content = css_content.replace(marker, desktop_floating_css.strip() + "\n\n" + marker)
    with open(CSS_PATH, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("Updated theme-modes.css with floating island styles!")
else:
    print("theme-modes.css already updated or marker not found")

# 2. Update unified-nav.js
with open(JS_PATH, 'r', encoding='utf-8') as f:
    js_content = f.read()

js_floating_rule = """
      @media (min-width: 993px) {
        #globalPortalNav {
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
        html.light #globalPortalNav {
          border: 1px solid rgba(15, 23, 42, 0.12) !important;
          box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.04) !important;
          background: rgba(255, 255, 255, 0.92) !important;
        }
      }
"""

js_marker = "@media (max-width: 992px) {"
if js_marker in js_content and "max-width: 1200px !important;" not in js_content:
    js_content = js_content.replace(js_marker, js_floating_rule.strip() + "\n      " + js_marker)
    with open(JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("Updated unified-nav.js with floating island styles!")
else:
    print("unified-nav.js already updated or marker not found")
