import json

with open(r'Capitoli_Divisi/Capitolo_08_segnali_indicazione/domande.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

def dump_range(start, end):
    for q in d['domande']:
        if start <= q['id'] <= end:
            print(f"ID {q['id']} ({q['risposta']}): {q['domanda']}")

dump_range(538, 603)
