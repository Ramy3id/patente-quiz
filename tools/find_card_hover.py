with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find card markup
card_tags = re.findall(r'<div[^>]*class="[^"]*(?:card|ch-|capitolo)[^"]*"', text, re.IGNORECASE)
for c in set(card_tags[:15]):
    print('Card markup:', c)

# Find CSS for card hover
css_blocks = re.findall(r'(\.[a-zA-Z0-9_\-]+(?::hover|:focus-within)[\s\S]*?\{[\s\S]*?\})', text)
for b in css_blocks:
    if 'card' in b.lower() or 'ch-' in b.lower() or 'capitolo' in b.lower():
        print('\n--- HOVER RULE ---')
        print(b)
