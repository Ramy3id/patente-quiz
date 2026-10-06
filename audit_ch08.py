import json
d = json.load(open(r'Capitoli_Divisi/Capitolo_08_segnali_indicazione/domande.json', encoding='utf-8'))
bad = []
for q in d['domande']:
    t, s, tr, pk = q.get('traduzione',''), q.get('spiegazione',''), q.get('trabocchetto',''), q.get('parole_chiave')
    if ('سؤال يتناول' in t or not t.strip() or not s.strip() or not tr.strip()
        or 'NO TRAP' in tr or 'ركز جيداً' in tr or not pk or len(pk) < 2
        or not (s.startswith('العبارة صحيحة') or s.startswith('العبارة خاطئة'))):
        bad.append(q['id'])
print('total', len(d['domande']), 'bad', len(bad), bad[:50])
