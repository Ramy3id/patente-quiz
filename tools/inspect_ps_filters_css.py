with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'[^{}]*ps-filters-row[^{]*\{[^}]*\}', html)
for m in matches:
    print(m)
matches2 = re.findall(r'[^{}]*ps-filter-btn[^{]*\{[^}]*\}', html)
for m in matches2[:3]:
    print(m)
