import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('bento-tools-section')
print("=== bento-tools-section ===")
print(content[idx:idx+4000])
