import sys

sys.stdout.reconfigure(encoding='utf-8')

for p in [r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html', r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html']:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    print(f"=== {p} ===")
    for line in c.splitlines():
        if any(k in line for k in ['chips', 'tabs', 'wrap', 'flex-wrap', 'grid-template']):
            if len(line.strip()) < 120:
                print("  ", line.strip())
