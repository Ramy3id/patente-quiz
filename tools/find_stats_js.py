with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'statWordsCount|statQuestionsCovered', text)]
with open(r'R:\Ramy\PATENTE_PRO_APP\tools\stats_js_updates.txt', 'w', encoding='utf-8') as out:
    for m in matches:
        out.write(text[m-80:m+200] + '\n---\n')
print('Saved stats JS updates.')
