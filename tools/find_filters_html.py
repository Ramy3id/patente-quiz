with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<div class=["\']ps-filters-row', text)]
print('Matches in HTML:', matches)
for m in matches:
    with open(r'R:\Ramy\PATENTE_PRO_APP\tools\filters_html.txt', 'w', encoding='utf-8') as out:
        out.write(text[m-200:m+1500])
print('Saved filters_html.txt')
