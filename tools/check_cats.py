import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\data_thesaurus.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
cats = re.findall(r'categoria:\s*["\']([^"\']+)["\']', text)
print(f'Total categories: {len(cats)}')
for i, c in enumerate(cats):
    print(f'{i+1}. {c}')
