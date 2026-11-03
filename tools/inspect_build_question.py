import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('buildQuestionCard(')
if idx != -1:
    print("buildQuestionCard found at", idx)
    print(text[idx:idx+2500])
else:
    # Let's search where `imgHtml` is used
    idx_img = text.find('imgHtml =')
    print("imgHtml found at", idx_img)
    print(text[idx_img-200:idx_img+1800])
