import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

# Find all occurrences of 'family-pill' or 'families-shelf' in non-CSS parts
for m in re.finditer(r'family-pill|families-shelf', parole):
    pos = m.start()
    # Check if in style
    style_start = parole.rfind('<style', 0, pos)
    style_end = parole.rfind('</style>', 0, pos)
    if style_start != -1 and (style_end == -1 or style_end < style_start):
        continue # inside style
    print(f"Non-style occurrence at {pos}:")
    print(parole[max(0, pos-100):min(len(parole), pos+300)])
    print("---------------------------------")
