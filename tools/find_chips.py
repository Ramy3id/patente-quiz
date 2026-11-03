with open(r'R:\Ramy\PATENTE_PRO_APP\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<div class="[^"]*filter[^"]*"[^>]*>[\s\S]*?</div>', html)
for m in matches[:5]:
    print(m[:300])
    print('---')
