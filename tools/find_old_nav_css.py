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

pages_with_old_nav_css = []
for p in html_files:
    rel = os.path.relpath(p, root_dir)
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    if 'max-height: calc(56px' in html or 'position: sticky' in html and 'unified-portal-nav' in html:
        pages_with_old_nav_css.append(rel)

print(f"Pages with old sticky navbar inline CSS ({len(pages_with_old_nav_css)}):")
for p in pages_with_old_nav_css:
    print(" -", p.encode('ascii', 'backslashreplace').decode('ascii'))
