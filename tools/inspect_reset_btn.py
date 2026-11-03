import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('chapter-reset-btn')
print("--- HTML in modular-chapter-engine.js ---")
print(text[idx-400:idx+400])

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', 'r', encoding='utf-8') as f:
    css = f.read()

idx_css = css.find('chapter-reset-btn')
print("\n--- CSS in modular-chapter.css ---")
if idx_css != -1:
    print(css[idx_css-100:idx_css+400])
else:
    print("Not found in modular-chapter.css")
