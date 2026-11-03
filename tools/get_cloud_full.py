with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m1 = re.search(r'حفظ بالسحابة', text)
if m1:
    start = max(0, m1.start() - 600)
    end = min(len(text), m1.end() + 200)
    with open(r'R:\Ramy\PATENTE_PRO_APP\tools\dash_cloud_full.txt', 'w', encoding='utf-8') as out:
        out.write(text[start:end])
print('Saved dash_cloud_full.txt')
