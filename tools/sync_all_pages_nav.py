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

target_version = "2026.11.05.V17_GLOBAL_UNIFIED_NAV"
updated_count = 0
cleaned_css_count = 0

for p in html_files:
    rel = os.path.relpath(p, root_dir)
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    orig = content
    
    # 1. Update theme-modes.css version query
    content = re.sub(r'theme-modes\.css(\?v=[^\'"]+)?', f'theme-modes.css?v={target_version}', content)
    
    # 2. Update unified-nav.js version query
    content = re.sub(r'unified-nav\.js(\?v=[^\'"]+)?', f'unified-nav.js?v={target_version}', content)
    
    # 3. Clean up old inline .unified-portal-nav { position: sticky; ... } blocks
    # Pattern to match old sticky unified-portal-nav rule
    old_sticky_pattern = re.compile(
        r'\.unified-portal-nav\s*\{[^}]*position:\s*sticky[^}]*\}',
        re.MULTILINE | re.DOTALL
    )
    if old_sticky_pattern.search(content):
        content = old_sticky_pattern.sub('/* old inline sticky nav removed */', content)
        cleaned_css_count += 1
        
    old_max_height_pattern = re.compile(
        r'\.unified-portal-nav\s*\{[^}]*max-height:\s*calc\(56px[^}]*\}',
        re.MULTILINE | re.DOTALL
    )
    if old_max_height_pattern.search(content):
        content = old_max_height_pattern.sub('/* old inline nav height removed */', content)
    
    if content != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1

print(f"Total HTML files updated with {target_version}: {updated_count}")
print(f"Total HTML files cleaned of old sticky inline CSS: {cleaned_css_count}")
