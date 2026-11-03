with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'[^{}]*ps-filters-row[^{]*\{[^}]*\}', html)
for m in matches:
    print('---')
    print(m)
