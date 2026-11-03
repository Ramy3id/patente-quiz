import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'html\.light', text)]
print('Matches for html.light in decodificatore-incroci.html:', len(matches))
for m in matches[:5]:
    print(text[m:m+200])
    print('---')
