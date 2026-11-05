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

cache_versions = {}

for p in html_files:
    rel = os.path.relpath(p, root_dir)
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    matches_css = re.findall(r'theme-modes\.css\?v=([^\'"]+)', html)
    matches_js = re.findall(r'unified-nav\.js\?v=([^\'"]+)', html)
    
    v_css = matches_css[0] if matches_css else ('no_v' if 'theme-modes.css' in html else 'none')
    v_js = matches_js[0] if matches_js else ('no_v' if 'unified-nav.js' in html else 'none')
    
    key = (v_css, v_js)
    if key not in cache_versions:
        cache_versions[key] = []
    cache_versions[key].append(rel)

for (v_css, v_js), pages in cache_versions.items():
    print(f"\n=== Version CSS: {v_css} | JS: {v_js} ({len(pages)} pages) ===")
    for p in pages[:5]:
        print(f"  - {p}")
    if len(pages) > 5:
        print(f"  ... and {len(pages)-5} more")
