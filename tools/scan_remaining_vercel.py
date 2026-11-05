import os, sys

sys.stdout.reconfigure(encoding='utf-8')

repo = r'R:\Ramy\PATENTE_PRO_APP'
matches = []

for root, dirs, files in os.walk(repo):
    if '.git' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.xml', '.txt', '.js', '.json')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'patente-quiz-livid.vercel.app' in c:
                    matches.append((p, c.count('patente-quiz-livid.vercel.app')))

print(f"Total remaining files with old Vercel URL: {len(matches)}")
for m in matches:
    print(" ", m[0], f"({m[1]} times)")
