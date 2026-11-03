import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'[^\n]{0,30}(?:02-10|11-13)[^\n]{0,30}', text):
    print(m.group(0))
