with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    code = f.read()

import re
matches = re.findall(r'[^{}]*footer-dev-card-compact[^{]*\{[^}]*\}', code)
for m in matches:
    print('---')
    print(m)
