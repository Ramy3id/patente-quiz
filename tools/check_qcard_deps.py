import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
terms = ['q-actions-row', 'status-', 'study-badge-', 'btn-explain-toggle', 'toggleDrawer', 'answerQuestion']
for t in terms:
    print(f"Occurrences of '{t}': {[m.start() for m in re.finditer(re.escape(t), text)]}")
