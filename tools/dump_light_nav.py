with open(r'R:\Ramy\PATENTE\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(html\.light\s*\.(?:nav-chapters-btn|nav-dropdown-tab|nav-search-trigger|nav-progress-pill|nav-theme-btn|nav-auth-pill)[^{]*\{[^}]+\})', text)
for m in matches:
    print('---')
    print(m.strip())
