import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', 'r', encoding='utf-8') as f:
    css = f.read()

idx = css.find('chapter-progress-meta')
print(css[idx-100:idx+400])
