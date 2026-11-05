import os
import re

root_dir = r'R:\Ramy\PATENTE_PRO_APP'

# Step 1: Check theme-modes.css rules for #globalPortalNav
with open(os.path.join(root_dir, r'assets\css\theme-modes.css'), 'r', encoding='utf-8') as f:
    css = f.read()

# Let's inspect all occurrences of #globalPortalNav in theme-modes.css
matches = re.findall(r'([^{}]*#globalPortalNav[^{}]*\{[^{}]*\})', css)
print(f"Total rules with #globalPortalNav in theme-modes.css: {len(matches)}")
for m in matches[:6]:
    print(" -", m.strip()[:100].encode('ascii', 'backslashreplace').decode('ascii'))
