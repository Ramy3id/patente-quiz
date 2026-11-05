import os
import re

root_dir = r'R:\Ramy\PATENTE_PRO_APP'

html_files = []
for root, dirs, files in os.walk(root_dir):
    if any(p in root for p in ['node_modules', '.git', 'tools']):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Total HTML files to inspect: {len(html_files)}")

results = []
for p in html_files:
    rel = os.path.relpath(p, root_dir)
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    has_unified_nav_script = 'unified-nav.js' in html
    has_theme_modes_css = 'theme-modes.css' in html
    has_static_nav = '<nav' in html
    has_header = '<header' in html
    
    # Check if there are other navbar classes or IDs
    other_navs = re.findall(r'<nav[^>]*id=[\'"]([^\'"]+)[\'"]', html)
    other_headers = re.findall(r'<header[^>]*id=[\'"]([^\'"]+)[\'"]', html)
    
    results.append({
        'rel': rel,
        'unified_nav': has_unified_nav_script,
        'theme_modes': has_theme_modes_css,
        'static_nav': has_static_nav,
        'other_navs': other_navs,
        'other_headers': other_headers
    })

# Group by status
no_unified = [r for r in results if not r['unified_nav']]
print(f"\nPages WITHOUT unified-nav.js ({len(no_unified)}):")
for r in no_unified:
    print(f" - {r['rel']}")

with_static_nav = [r for r in results if r['static_nav'] and r['unified_nav']]
print(f"\nPages WITH static <nav> AND unified-nav.js ({len(with_static_nav)}):")
for r in with_static_nav[:10]:
    print(f" - {r['rel']} (other_navs: {r['other_navs']})")
