import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'renderQuestion', text)]
print('Matches for renderQuestion:', matches)

for m in matches:
    print('--- MATCH ---')
    print(text[m:m+800])

# Also let's find `q-card` or how each question HTML is built
matches_card = [m.start() for m in re.finditer(r'<div class="q-card', text)]
print('Matches for <div class="q-card:', matches_card)
for m in matches_card:
    print('--- Q-CARD HTML SNIPPET ---')
    print(text[m:m+1200])
