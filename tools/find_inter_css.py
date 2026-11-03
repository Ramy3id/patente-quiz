import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\interactive_style.css'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("File size:", len(content))
for line in content.splitlines():
    if any(k in line.lower() for k in ['choice', 'btn-vf', 'vero', 'falso', 'grid', 'flex']):
        print(line[:100])
