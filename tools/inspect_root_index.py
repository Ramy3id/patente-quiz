import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE_PRO_APP\index.html', 'r', encoding='utf-8') as f:
    print(f.read()[:500])
