import os, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for root, dirs, files in os.walk('R:/Ramy/PATENTE_PRO_APP'):
    if 'node_modules' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith(('.js', '.html')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'theme' in c.lower() and 'localstorage' in c.lower():
                    print(f"Theme in {p}")
                    import re
                    for m in re.finditer(r'localStorage\.(?:get|set)Item\([^)]+\)', c):
                        print("  ", m.group(0))
