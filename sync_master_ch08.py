import json
mp = r'assets/all_questions.json'
src = json.load(open(r'Capitoli_Divisi/Capitolo_08_segnali_indicazione/domande.json', encoding='utf-8'))['domande']
by_id = {q['id']: q for q in src}
master = json.load(open(mp, encoding='utf-8'))
n = 0
for q in master:
    if str(q.get('capitolo_num')).lstrip('0') == '8' and q['id'] in by_id:
        s = by_id[q['id']]
        for k in ('traduzione', 'spiegazione', 'trabocchetto', 'parole_chiave'):
            q[k] = s[k]
        n += 1
json.dump(master, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('synced', n)
