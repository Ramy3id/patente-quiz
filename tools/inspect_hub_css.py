with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'[^{}]*(?:exam-control-hub|exam-nav-pills|hub-primary-row)[^{]*\{[^}]*\}', html)
for m in matches:
    print('---')
    print(m)
