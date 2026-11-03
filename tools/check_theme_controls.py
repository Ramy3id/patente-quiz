import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'(?:controls-bar|search-box|filter-btns-wrap|f-btn)', text)]
print('Matches in theme-modes.css:', len(matches))
for m in matches[:5]:
    print(text[m-30:m+150])
    print('---')
