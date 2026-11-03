import sys

sys.stdout.reconfigure(encoding='utf-8')

for p in [
    r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\interactive_style.css',
    r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
]:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'choice-grid' in c or 'btn-vf' in c or 'btn-vero' in c or 'btn-falso' in c:
        print(f"FOUND IN {p}")
        for line in c.splitlines():
            if any(k in line for k in ['choice', 'vero', 'falso', 'btn-vf']):
                print("  ", line)
    else:
        print(f"NOT found in {p}")
