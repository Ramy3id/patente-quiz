import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', 'r', encoding='utf-8') as f:
    css = f.read()

idx = css.find('subtopic-section-header')
if idx != -1:
    print("--- subtopic-section-header in CSS ---")
    print(css[idx-50:idx+500])

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx2 = js.find('subtopic-header-stats')
if idx2 != -1:
    print("--- HTML in JS ---")
    print(js[idx2-300:idx2+600])
