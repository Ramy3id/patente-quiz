import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'toggleTheme|theme', text, re.IGNORECASE)]
print("Matches in unified-nav.js:", len(matches))
for m in matches[:6]:
    print(text[m-30:m+200])
    print('---')
