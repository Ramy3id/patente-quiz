import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

idx = parole.find('.families-shelf')
while idx != -1:
    print("=== .families-shelf CSS/JS snippet ===")
    print(parole[max(0, idx-100):min(len(parole), idx+600)])
    print("---------------------------------------")
    idx = parole.find('.families-shelf', idx+1)
