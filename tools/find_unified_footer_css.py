import glob
import os
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for root, dirs, files in os.walk('R:/Ramy/PATENTE_PRO_APP'):
    if 'node_modules' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith(('.js', '.css', '.html')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'unified-portal-footer' in c:
                    print(f"Found in {p}")
