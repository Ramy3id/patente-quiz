import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('tools-hub-grid')
if idx != -1:
    print(content[idx:idx+1500])
