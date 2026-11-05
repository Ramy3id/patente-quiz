import os, sys

sys.stdout.reconfigure(encoding='utf-8')

repo = r'R:\Ramy\PATENTE_PRO_APP'

for root, dirs, files in os.walk(repo):
    if '.git' in root: continue
    for f in files:
        if f.endswith(('.html', '.js')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'footer-cache-reset-btn' in c:
                    print("Found footer-cache-reset-btn in:", p)
                if 'footer-dev-avatar-wrapper' in c:
                    print("Found footer-dev-avatar-wrapper in:", p)
