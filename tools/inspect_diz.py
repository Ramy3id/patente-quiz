import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html', 'r', encoding='utf-8') as f:
    diz = f.read()

for term in ['PATENTE_THESAURUS', 'Velocità', 'families', 'pills']:
    idx = diz.find(term)
    print(f"dizionario-sinonimi term '{term}': {idx}")
