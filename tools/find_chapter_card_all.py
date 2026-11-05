with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\.chapter-card[\s\S]*?\{[\s\S]*?\})', text)
for m in matches:
    print('--- MATCH IN index.html ---')
    print(m)
