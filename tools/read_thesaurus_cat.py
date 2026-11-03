import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\data_thesaurus.js', 'r', encoding='utf-8') as f:
    text = f.read()

items = re.findall(r'categoria:\s*["\']([^"\']+)["\']', text)
print('Count:', len(items))
for it in items:
    print('-', it)
