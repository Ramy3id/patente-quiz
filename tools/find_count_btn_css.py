import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'tr-count-btn', content)]
for p in matches:
    print(content[max(0, p-40):min(len(content), p+140)])
    print("="*30)
