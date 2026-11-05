import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update assets/js/unified-nav.js
nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Add arrowLeft to SVG_ICONS
arrow_svg_def = """    arrowLeft: '<svg class="ui-svg btn-arrow-svg" viewBox="0 0 24 24" style="width:15px;height:15px;stroke-width:2.5;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;margin-right:6px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',"""

if 'arrowLeft:' not in nav:
    nav = nav.replace("    play:", arrow_svg_def + "\n    play:")

# Update study button hydration
old_hyd = """      // 2. فحص أزرار بدء المذاكرة
      document.querySelectorAll('.btn-action-study, .btn-study, .study-btn').forEach(btn => {
        if (btn.querySelector('svg')) return;
        if (btn.textContent.includes('بدء المذاكرة') || btn.textContent.includes('🎯')) {
          btn.innerHTML = '<span>' + SVG_ICONS.play + ' ' + btn.textContent.replace('🎯', '').trim() + '</span>';
        }
      });"""

new_hyd = """      // 2. فحص أزرار بدء المذاكرة
      document.querySelectorAll('.btn-action-study, .btn-study, .study-btn').forEach(btn => {
        if (btn.querySelector('.btn-arrow-svg')) return;
        const text = btn.textContent.replace('🎯', '').replace('▷', '').replace('◁', '').trim();
        btn.innerHTML = '<span>' + text + '</span>' + SVG_ICONS.arrowLeft;
      });"""

if old_hyd in nav:
    nav = nav.replace(old_hyd, new_hyd)
else:
    print("WARNING: old_hyd not matched exactly, checking fallback...")
    import re
    nav = re.sub(
        r'// 2\. فحص أزرار بدء المذاكرة[\s\S]*?\}\);\n',
        new_hyd + '\n',
        nav
    )

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)
print("SUCCESS: Updated unified-nav.js with arrowLeft")

# 2. Update assets/css/theme-modes.css
css_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

btn_arrow_css = """
.btn-action-study {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  direction: rtl !important;
  gap: 8px !important;
}

.btn-action-study .btn-arrow-svg {
  width: 15px !important;
  height: 15px !important;
  stroke-width: 2.5 !important;
  fill: none !important;
  stroke: currentColor !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
  margin-right: 6px !important;
  margin-left: 0 !important;
  flex-shrink: 0 !important;
  transition: transform 0.2s ease !important;
}

.btn-action-study:hover .btn-arrow-svg {
  transform: translateX(-3px) !important;
}
"""

if '.btn-action-study .btn-arrow-svg' not in css:
    css += btn_arrow_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("SUCCESS: Added arrow CSS to theme-modes.css")
else:
    print("NOTE: CSS already present")
