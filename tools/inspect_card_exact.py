import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('if (this.isQuestionLocked(q))')
idx2 = text.find('renderQuestions() {')

print("--- QUESTION RENDERING CODE (lines ~20500 to ~23500) ---")
print(text[idx1-50:idx2])
