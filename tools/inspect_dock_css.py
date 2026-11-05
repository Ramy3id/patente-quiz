import sys

sys.stdout.reconfigure(encoding='utf-8')

for p in [r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css']:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    idx = 0
    print(f"=== File: {p} ===")
    while True:
        idx = c.find('mobile-dock', idx)
        if idx == -1:
            idx = c.find('mobileBottomNav', 0) if idx == 0 else -1
            if idx == -1: break
        print(c[max(0, idx-80):min(len(c), idx+200)].replace('\n', ' '))
        print("---")
        break
