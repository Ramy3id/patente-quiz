import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

root = r'R:\Ramy\PATENTE_PRO_APP'

for p in [
    r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html',
    r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html',
    r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\laboratorio-numeri.html',
    r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
]:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'tabs' in c or 'overflow-x' in c or 'chips-scroll' in c or 'scroll' in c:
        print(f"=== SCROLL IN {os.path.basename(p)} ===")
        for line in c.splitlines():
            if any(k in line for k in ['overflow-x', 'scroll-snap', 'scrollbar', 'mask-image', 'snap_scroll']):
                print("  ", line.strip())
