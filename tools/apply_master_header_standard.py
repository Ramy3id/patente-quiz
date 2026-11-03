import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Update theme-modes.css
with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

master_rules = """
/* ==========================================================================
   MASTER UNIFIED HEADER SPECIFICATION & CONTENT SPACING (Apple HIG)
   Guarantees 100% frozen / identical header size, position & content distance
   ========================================================================== */
#globalPortalNav,
.unified-portal-nav {
  position: sticky !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  width: 100% !important;
  height: 56px !important;
  min-height: 56px !important;
  max-height: 56px !important;
  z-index: 10000 !important;
  margin: 0 !important;
  padding: 0 16px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  box-sizing: border-box !important;
  background: rgba(11, 15, 25, 0.94) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15) !important;
  direction: rtl !important;
}

html.light #globalPortalNav,
html.light .unified-portal-nav {
  background: rgba(255, 255, 255, 0.96) !important;
  border-bottom: 1px solid rgba(15, 23, 42, 0.09) !important;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
}

/* Master Baseline Content Spacing Below Frozen Header */
@media (max-width: 768px) {
  .container,
  .ps-container,
  .exam-portal-container,
  .dash-wrapper,
  .dict-container,
  .zm-container,
  .tr-container,
  .cq-container {
    margin-top: 12px !important;
    padding-top: 0 !important;
    box-sizing: border-box !important;
  }

  .guest-free-sample-banner {
    margin: 12px 16px 0 !important;
    border-radius: 14px !important;
    padding: 12px 14px !important;
    box-sizing: border-box !important;
    background: rgba(234, 179, 8, 0.12) !important;
    border: 1px solid rgba(234, 179, 8, 0.3) !important;
  }
}
"""

if "MASTER UNIFIED HEADER SPECIFICATION" not in css_content:
    css_content += master_rules
    with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("SUCCESS: added master header standard to theme-modes.css")
else:
    print("INFO: master header standard already present in theme-modes.css")

# 2. Update unified-nav.js nav height
with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

js_content = js_content.replace('min-height: 60px;', 'height: 56px; min-height: 56px; max-height: 56px;')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("SUCCESS: updated unified-nav.js to 56px")
