with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.footer-dev-card[^{]*\{[^}]*\})', css)
for m in matches:
    print('---')
    print(m)
