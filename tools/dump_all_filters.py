with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<div class=["\']ps-filters-row', text)]
for i, m in enumerate(matches):
    with open(f'R:\\Ramy\\PATENTE_PRO_APP\\tools\\filters_html_{i+1}.txt', 'w', encoding='utf-8') as out:
        out.write(text[m-200:m+1200])
print('Saved all 3 filters matches.')
