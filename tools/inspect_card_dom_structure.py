import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('buildQuestionCard(')
if idx == -1:
    idx = text.find('q-answers-grid')
print(text[idx-100:idx+1200])
