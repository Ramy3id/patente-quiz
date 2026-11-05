import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

# Search for mentions of thesaurus or category pills
for term in ['THESAURUS', 'thesaurus', 'clusters', 'topics', 'filter-pill', 'pills']:
    matches = list(re.finditer(re.escape(term), parole, re.IGNORECASE))
    print(f"Found {len(matches)} occurrences of '{term}'")
    if matches and len(matches) < 10:
        for m in matches:
            print("  snippet:", parole[max(0, m.start()-50):min(len(parole), m.end()+100)].replace('\n', ' '))
