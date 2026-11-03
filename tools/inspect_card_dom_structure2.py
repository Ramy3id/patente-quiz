import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('return `\n        <div class="${cardClass}" id="q-card-${q.id}">')
if idx == -1:
    idx = text.find('<div class="${cardClass}" id="q-card-${q.id}">')
print(text[idx:idx+1500])
