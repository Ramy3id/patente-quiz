import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'answerQuestion[^{]*\{', text):
    print(m.group(0), "at", m.start())
    print(text[m.start():m.start()+800])
    print("="*40)
