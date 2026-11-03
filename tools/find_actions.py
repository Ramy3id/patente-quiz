import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'تصفح الباب|cq-card-actions|cq-action-btn', text)]
for idx in matches[:5]:
    print(text[max(0, idx-100):min(len(text), idx+150)])
    print('---')
