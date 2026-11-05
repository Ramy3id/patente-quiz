import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for m in re.finditer(r'ابحث باسم الباب', html):
    start = max(0, m.start() - 200)
    end = min(len(html), m.end() + 200)
    print(html[start:end])
    print('='*50)
