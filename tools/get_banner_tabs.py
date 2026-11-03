with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m1 = re.search(r'حفظ بالسحابة', text)
if m1:
    start = max(0, m1.start() - 1200)
    end = min(len(text), m1.end() + 600)
    with open(r'R:\Ramy\PATENTE_PRO_APP\tools\dash_banner_and_tabs.txt', 'w', encoding='utf-8') as out:
        out.write(text[start:end])
print('Saved dash_banner_and_tabs.txt')
