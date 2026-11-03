import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'fig-modal-card' in l or 'fig-modal-search' in l:
        print(f"{i+1}: {l.strip()}")
