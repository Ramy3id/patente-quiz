import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('application/ld+json')
if idx != -1:
    print(c[idx:idx+1200])
