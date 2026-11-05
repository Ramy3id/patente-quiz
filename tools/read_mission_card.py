import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.findall(r'<section[^>]*class=["\']sp-mission-card["\'][^>]*>[\s\S]*?</section>', text)
if m:
    print('Found sp-mission-card, length:', len(m[0]))
    print(m[0][:1500])
else:
    print('sp-mission-card not found')
