import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

root = r'R:\Ramy\PATENTE_PRO_APP'
html_files = []
for dirpath, dirnames, filenames in os.walk(root):
    if '.git' in dirpath:
        continue
    for f in filenames:
        if f.endswith('.html'):
            html_files.append(os.path.relpath(os.path.join(dirpath, f), root))

for h in sorted(html_files):
    print(h)
