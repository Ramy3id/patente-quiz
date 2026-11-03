import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', 'r', encoding='utf-8') as f:
    css = f.read()

for sel in ['subtopic-header-stats', 'subtopic-stat-pill', 'subtopic-mastery-badge']:
    idx = css.find(sel)
    print(f"\n--- {sel} ---")
    if idx != -1:
        print(css[idx-50:idx+300])
    else:
        print("Not found")
