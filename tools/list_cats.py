import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json, re

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\data_thesaurus.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const PATENTE_THESAURUS\s*=\s*(\[.*?\]);', text, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print(f"Total items: {len(data)}")
    for i, d in enumerate(data):
        print(f"{i+1}. id={d['id']} | cat={d['categoria']} | base={d['parola_base']}")
