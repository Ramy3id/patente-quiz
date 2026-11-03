import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const PATENTE_THESAURUS\s*=\s*\[([\s\S]*?)\];', text)
if m:
    items = re.findall(r'categoria:\s*[\'"]([^\'"]+)[\'"]', m.group(1))
    print('Thesaurus categories count:', len(items))
    for it in items:
        print('-', it)
