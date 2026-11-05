import os, sys

sys.stdout.reconfigure(encoding='utf-8')

repo = r'R:\Ramy\PATENTE_PRO_APP'

for root, dirs, files in os.walk(repo):
    if '.git' in root: continue
    for f in files:
        if f.endswith(('.html', '.css', '.js')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'nav-mobile-hamburger' in c or 'nav-mobile-btn' in c or 'btnToggleMobileDrawer' in c:
                    if p.endswith('unified-nav.js'): continue
                    print("Found override in:", p)
                    for t in ['nav-mobile-hamburger', 'nav-mobile-btn', 'btnToggleMobileDrawer']:
                        idx = c.find(t)
                        if idx != -1:
                            print(f"  {t} snippet:", c[max(0, idx-40):min(len(c), idx+120)].replace('\n', ' '))
