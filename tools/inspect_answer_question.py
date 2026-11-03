import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('answerQuestion(id, choice)')
if idx == -1:
    idx = text.find('answerQuestion(')
print(text[idx:idx+2500])
