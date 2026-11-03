import sys

sys.stdout.reconfigure(encoding='utf-8')

for p in [r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html', r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\interactive_style.css']:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'tr-back-link' in c:
        print("Found in", p)
        for line in c.splitlines():
            if 'tr-back-link' in line or 'tr-top-nav' in line:
                print("  ", line)
