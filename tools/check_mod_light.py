import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\modular-chapter.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'html\.light[^{]+', text)
print(f"Total html.light matches in modular-chapter.css: {len(matches)}")
for m in matches[:15]:
    print('-', m.strip())
