import json
from collections import defaultdict

with open(r'Capitoli_Divisi/Capitolo_08_segnali_indicazione/domande.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

groups = defaultdict(list)
for q in d['domande']:
    if q['id'] >= 352:
        key = (q.get('sotto_argomento'), q.get('immagine'))
        groups[key].append(q)

for (sa, img), qs in groups.items():
    print(f"[{min(q['id'] for q in qs)}..{max(q['id'] for q in qs)}] ({len(qs)} qs) | Sub: {sa} | Img: {img}")
