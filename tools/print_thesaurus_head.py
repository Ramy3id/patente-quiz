import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\data_thesaurus.js', 'r', encoding='utf-8') as f:
    for i in range(40):
        print(f.readline(), end='')
