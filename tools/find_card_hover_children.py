with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\.chapter-card:hover[\s\S]*?\{[\s\S]*?\})', text)
for m in matches:
    print('Hover rule:', m)

# Also check button inside card
btn_rules = re.findall(r'(\.(?:btn-start|card-btn|action-btn)[\s\S]*?\{[\s\S]*?\})', text)
for b in btn_rules[:5]:
    print('Btn rule:', b)
