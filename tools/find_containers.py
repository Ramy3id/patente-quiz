import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

# Find the HTML container holding chips-actions
idx = parole.find('class="chips-actions"')
if idx != -1:
    print("=== HTML around chips-actions ===")
    print(parole[idx-400:idx+400])

# Find the HTML container holding segmented-filter-bar
idx2 = parole.find('class="segmented-filter-bar"')
if idx2 != -1:
    print("=== HTML around segmented-filter-bar ===")
    print(parole[idx2-300:idx2+400])
