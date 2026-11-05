with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\.btn-action-study[\s\S]*?\{[\s\S]*?\})', text)
for i in [3, 4]:
    print(matches[i])
