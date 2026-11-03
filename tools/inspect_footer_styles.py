import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for p in ['R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js']:
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"\n=== {p} ===")
    import re
    for m in re.finditer(r'unified-portal-footer', text):
        idx = m.start()
        print(text[max(0, idx-50):min(len(text), idx+500)])
        print("-" * 40)
