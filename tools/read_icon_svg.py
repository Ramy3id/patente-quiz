import sys

sys.stdout.reconfigure(encoding='utf-8')
p = r'R:\Ramy\PATENTE_PRO_APP\assets\icons\icon.svg'
with open(p, 'r', encoding='utf-8') as f:
    print(f.read())
