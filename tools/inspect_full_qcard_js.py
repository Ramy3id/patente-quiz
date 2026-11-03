import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('buildQuestionCard(')
if idx != -1:
    end_idx = text.find('renderQuestions() {', idx)
    print(text[idx:end_idx if end_idx != -1 else idx+4000])
else:
    # Let's search where `return \`\s*<div class="${cardClass}"` is
    idx2 = text.find('<div class="${cardClass}"')
    print(text[idx2-200:idx2+2500])
