import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    if any(k in line for k in ['href=', 'معمل', 'مفكك', 'رادار', 'خزينة', 'محاكي', 'مفاهيم', 'كتل', 'decodificatore', 'parole-spia', 'laboratorio']):
        print(line.strip())
