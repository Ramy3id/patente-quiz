import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'fig-modal', text)]
print("fig-modal occurrences:", len(matches))
for m in matches:
    print(text[m-20:m+250])
    print('='*40)
