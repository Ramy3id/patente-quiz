with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.findall(r'(\.footer-dev[^{]*\{[^}]*\})', js)
print('Matches in unified-nav.js:', len(matches))
for m in matches:
    print('---')
    print(m)
