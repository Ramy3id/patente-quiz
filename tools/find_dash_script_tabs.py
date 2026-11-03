with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'dash-tab-btn|dash-tabs-bar', text)]
with open(r'R:\Ramy\PATENTE_PRO_APP\tools\dash_script_tabs.txt', 'w', encoding='utf-8') as out:
    for m in matches:
        out.write(text[m-50:m+150] + '\n---\n')
print(f'Found {len(matches)} matches.')
