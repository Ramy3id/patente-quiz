import sys

sys.stdout.reconfigure(encoding='utf-8')
p = r'R:\Ramy\PATENTE_PRO_APP\service-worker.js'
with open(p, 'r', encoding='utf-8') as f:
    print(f.read()[:2000])
