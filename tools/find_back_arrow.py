import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
for m in re.finditer(r'tr-back-arrow', content):
    pos = m.start()
    print(content[max(0, pos-40):min(len(content), pos+80)])
