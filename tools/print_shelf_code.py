import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

idx = parole.find('function renderThesaurusShelf')
if idx != -1:
    print(parole[idx:idx+1500])
else:
    # search around 86570
    print(parole[86000:87500])
