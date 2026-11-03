with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'[^{}]*(?:skin-moto|motoScreenWrap|modernScreenWrap)[^{]*\{[^}]*\}', html)
for m in matches[:6]:
    print('---')
    print(m)
