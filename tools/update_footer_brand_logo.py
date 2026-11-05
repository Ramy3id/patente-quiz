import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update unified-nav.js
nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

old_brand_header = '''              <div class="footer-brand-header">
                <span class="footer-brand-icon">🚦</span>
                <span class="footer-brand-title">Patente B Pro</span>
                <span class="footer-brand-year">2026</span>
              </div>'''

new_brand_header = '''              <div class="footer-brand-header">
                <span class="footer-brand-year">2026</span>
                <span class="footer-brand-title">Patente B Pro</span>
                <img src="${ctx.root}assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" class="footer-brand-logo" width="30" height="30" style="width:30px; height:30px; object-fit:contain; border-radius:50%; flex-shrink:0;">
              </div>'''

if old_brand_header in nav:
    nav = nav.replace(old_brand_header, new_brand_header, 1)
    print("Replaced footer brand header in unified-nav.js successfully.")
else:
    print("WARNING: old_brand_header not found!")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# 2. Update theme-modes.css
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

footer_logo_css = '''
.footer-brand-logo {
  width: 30px !important;
  height: 30px !important;
  min-width: 30px !important;
  min-height: 30px !important;
  border-radius: 50% !important;
  object-fit: contain !important;
  flex-shrink: 0 !important;
}
'''

tm += '\n' + footer_logo_css

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("Updated theme-modes.css with footer brand logo styles.")
