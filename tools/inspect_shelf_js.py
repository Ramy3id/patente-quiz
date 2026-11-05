import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

# Let's see how families-shelf is rendered in JS
idx = parole.find('families-shelf')
while idx != -1:
    if 'render' in parole[max(0, idx-100):min(len(parole), idx+300)]:
        print("=== JS around families-shelf ===")
        print(parole[max(0, idx-150):min(len(parole), idx+400)])
        break
    idx = parole.find('families-shelf', idx+1)

# Check renderFamilies or similar
for fn in ['renderFamilies', 'renderThesaurus', 'renderShelf', 'buildFamilies']:
    idx = parole.find(fn)
    if idx != -1:
        print(f"=== Found function {fn} ===")
        print(parole[idx:idx+500])
