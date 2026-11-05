import os, sys

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk(r'R:\Ramy\PATENTE_PRO_APP'):
    for f in files:
        if f.endswith('.css') or f.endswith('.js'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'nav-mobile-hamburger' in c or 'hamburger-box' in c:
                    print("Found in:", p)
                    for term in ['nav-mobile-hamburger', 'hamburger-box']:
                        idx = c.find(term)
                        if idx != -1:
                            print(f"  term '{term}' snippet:")
                            print("  " + c[max(0, idx-50):min(len(c), idx+150)].replace('\n', ' '))
