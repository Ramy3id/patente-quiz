import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html', 'r', encoding='utf-8') as f:
    diz = f.read()

idx = diz.find('PATENTE_THESAURUS')
print("=== dizionario around PATENTE_THESAURUS ===")
print(diz[max(0, idx-100):min(len(diz), idx+800)])
