import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Update unified-nav.js
with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    nav_code = f.read()

old_footer_tag = '<footer class="unified-portal-footer" id="globalPortalFooter" role="contentinfo">'
new_footer_tag = '<footer class="unified-portal-footer" id="globalPortalFooter" role="contentinfo" dir="rtl">'

if old_footer_tag in nav_code:
    nav_code = nav_code.replace(old_footer_tag, new_footer_tag, 1)
    print("SUCCESS: Added dir='rtl' to footer in unified-nav.js")
else:
    print("WARNING: old_footer_tag not found in unified-nav.js")

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'w', encoding='utf-8') as f:
    f.write(nav_code)


# 2. Update theme-modes.css
with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'r', encoding='utf-8') as f:
    tm_css = f.read()

old_tm_footer = '''.unified-portal-footer {
  margin-top: 60px !important;
  background: #0B0F19 !important;
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding: 48px 24px 120px !important;
  color: #94A3B8 !important;
  box-sizing: border-box !important;
  width: 100% !important;
}'''

new_tm_footer = '''.unified-portal-footer {
  margin-top: 60px !important;
  background: #0B0F19 !important;
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding: 48px 24px 120px !important;
  color: #94A3B8 !important;
  box-sizing: border-box !important;
  width: 100% !important;
  direction: rtl !important;
  text-align: right !important;
}'''

if old_tm_footer in tm_css:
    tm_css = tm_css.replace(old_tm_footer, new_tm_footer, 1)
    print("SUCCESS: Updated .unified-portal-footer in theme-modes.css")
else:
    print("WARNING: old_tm_footer not found in theme-modes.css")

# Also ensure RTL for footer children in theme-modes.css
rtl_footer_children = """
/* Footer RTL Text Alignment Guarantee */
.unified-portal-footer,
.unified-portal-footer * {
  box-sizing: border-box;
}

.unified-portal-footer .footer-container,
.unified-portal-footer .footer-top-grid,
.unified-portal-footer .footer-col,
.unified-portal-footer .footer-col-brand,
.unified-portal-footer .footer-brand-desc,
.unified-portal-footer .footer-col-title,
.unified-portal-footer .footer-nav-list,
.unified-portal-footer .footer-nav-link {
  direction: rtl !important;
  text-align: right !important;
}

.unified-portal-footer .footer-brand-header {
  direction: rtl !important;
  justify-content: flex-start !important;
}

.unified-portal-footer .footer-brand-stats {
  direction: rtl !important;
  justify-content: flex-start !important;
}
"""

if 'Footer RTL Text Alignment Guarantee' not in tm_css:
    tm_css += rtl_footer_children
    print("SUCCESS: Appended Footer RTL Text Alignment Guarantee to theme-modes.css")

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'w', encoding='utf-8') as f:
    f.write(tm_css)


# 3. Update modular-chapter.css
with open('R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', 'r', encoding='utf-8') as f:
    mc_css = f.read()

if 'Footer RTL Text Alignment Guarantee' not in mc_css:
    mc_css += rtl_footer_children
    print("SUCCESS: Appended Footer RTL Text Alignment Guarantee to modular-chapter.css")

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', 'w', encoding='utf-8') as f:
    f.write(mc_css)

print("Done applying RTL updates to footer!")
