with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'guestSyncBanner|حفظ بالسحابة', text)
if m:
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 300)
    with open(r'R:\Ramy\PATENTE_PRO_APP\tools\banner_context.txt', 'w', encoding='utf-8') as out:
        out.write(text[start:end])
print('Saved banner context.')
