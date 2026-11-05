import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# 1. In renderGlobalHeader(): replace brand-emoji with new brand-logo-img
old_brand_html = '''          <a href="${ctx.capitoli}index.html" class="nav-brand" title="الرئيسية — Patente B Pro">
            <span class="brand-emoji">🚦</span>
            <span class="brand-text">Patente B Pro</span>
            <span class="badge-tag">2026</span>
          </a>'''

new_brand_html = '''          <a href="${ctx.capitoli}index.html" class="nav-brand" title="الرئيسية — Patente B Pro" style="direction: ltr !important;">
            <img src="${ctx.root}assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" class="brand-logo-img" width="28" height="28" style="width:28px; height:28px; object-fit:contain; border-radius:50%; box-shadow: 0 2px 8px rgba(0,0,0,0.35); flex-shrink:0;">
            <span class="brand-text">Patente B Pro</span>
            <span class="badge-tag">2026</span>
          </a>'''

if old_brand_html in nav:
    nav = nav.replace(old_brand_html, new_brand_html, 1)
    print("Replaced brand emoji in header with official logo.")
else:
    print("WARNING: old_brand_html not found")

# 2. In drawer header: update logo
old_drawer_brand = '''            <!-- الشعار والاسم على اليسار ليتطابق مع هيدر التطبيق الرئيسي -->
            <div class="drawer-header-brand">
              <div>
                <strong class="drawer-app-title">Patente B Pro</strong>
                <span class="drawer-app-subtitle">القائمة الموحدة وتصفح الأبواب</span>
              </div>
              <span style="font-size:1.4rem;">🚦</span>
            </div>'''

new_drawer_brand = '''            <!-- الشعار والاسم على اليسار ليتطابق مع هيدر التطبيق الرئيسي -->
            <div class="drawer-header-brand" style="direction: ltr !important; display: flex !important; align-items: center !important; gap: 10px !important;">
              <img src="${ctx.root}assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" class="brand-logo-img" width="30" height="30" style="width:30px; height:30px; object-fit:contain; border-radius:50%; box-shadow: 0 2px 8px rgba(0,0,0,0.35); flex-shrink:0;">
              <div style="text-align: left;">
                <strong class="drawer-app-title">Patente B Pro</strong>
                <span class="drawer-app-subtitle">القائمة الموحدة وتصفح الأبواب</span>
              </div>
            </div>'''

if old_drawer_brand in nav:
    nav = nav.replace(old_drawer_brand, new_drawer_brand, 1)
    print("Replaced brand emoji in drawer with official logo.")
else:
    print("WARNING: old_drawer_brand not found")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# 3. Update theme-modes.css to ensure .nav-brand has direction: ltr
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

brand_css = '''
/* Official Brand Steering Wheel Logo Styling (Left-Aligned in Header) */
.nav-brand {
  direction: ltr !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}

.nav-brand .brand-logo-img {
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  min-height: 28px !important;
  border-radius: 50% !important;
  object-fit: contain !important;
  flex-shrink: 0 !important;
}
'''

tm += '\n' + brand_css

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("Updated theme-modes.css with brand logo rules.")
