import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
app_dir = r'R:\Ramy\PATENTE_PRO_APP'

for root, dirs, files in os.walk(app_dir):
    dirs[:] = [d for d in dirs if d != 'node_modules' and d != '.git']
    for f in files:
        if f.endswith(('.html', '.js', '.json', '.bat', '.txt', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    if 'vercel' in content.lower():
                        matches = [line.strip() for line in content.split('\n') if 'vercel' in line.lower()]
                        print(f'=== {f} ===')
                        for m in matches[:5]:
                            print(' ', m[:120])
            except Exception:
                pass
