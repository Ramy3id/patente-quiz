# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

links = set(re.findall(r'href=[\'"]([^\'"]+\.html)[\'"]', text))
print("Links in unified-nav.js:")
for l in sorted(links):
    print(" -", l)
