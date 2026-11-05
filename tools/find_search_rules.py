import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for s in ['.search-wrapper', '.search-icon', '.search-input', '.search-shortcut']:
    idx = content.find(s)
    if idx != -1:
        print(f"=== {s} ===")
        print(content[idx:idx+300])
        print("-------------")
