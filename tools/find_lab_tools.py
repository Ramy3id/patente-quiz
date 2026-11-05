import os, sys

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk(r'R:\Ramy\PATENTE_PRO_APP'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'المعامل' in c or 'الأدوات' in c or 'piano-studio' in c:
                    print(f"Match in {p}:")
                    for term in ['المعامل', 'piano-studio']:
                        idx = c.find(term)
                        if idx != -1:
                            print(f"  term '{term}' found at {idx}:")
                            print("  " + c[max(0, idx-80):min(len(c), idx+160)].replace('\n', ' '))
