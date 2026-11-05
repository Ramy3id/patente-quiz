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
                for kw in ['حذف الكاش', 'تحديث المنصة', 'Eng. Ramy Fahmy', 'Software Architecture Engineer']:
                    if kw in c:
                        print(f"Found '{kw}' in {p}")
                        idx = c.find(kw)
                        print("  Snippet:", c[max(0, idx-60):min(len(c), idx+180)].replace('\n', ' '))
                        print("------------------")
