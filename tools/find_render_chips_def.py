import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'renderChips\s*\(\)\s*\{', text)]
for idx in matches:
    print(text[idx:idx+1500])
    print('='*50)
