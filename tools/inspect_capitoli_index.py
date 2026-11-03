import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '02-10' in l or 'filter' in l.lower() or 'search' in l.lower():
        if '<button' in l or 'onclick' in l or '<input' in l or 'function' in l:
            print(f"{i+1}: {l.strip()[:100]}")
