import json, re
f = 'Simulatore_Esame.html'
h = open(f, encoding='utf-8').read()
src = json.load(open(r'Capitoli_Divisi/Capitolo_08_segnali_indicazione/domande.json', encoding='utf-8'))['domande']
by_q = {}
for q in src:
    by_q.setdefault(q['domanda'].strip().rstrip('.'), []).append(q)

idx = h.find('"ch": 8,')
starts = [m for m in re.finditer(r'(const|let|var)\s+(\w+)\s*=\s*\[', h) if m.end() <= idx]
m = starts[-1]
s = m.end() - 1
arr, length = json.JSONDecoder().raw_decode(h[s:])
print('var', m.group(2), 'items', len(arr))
n = miss = 0
used = {}
for it in arr:
    if it.get('ch') != 8:
        continue
    key = it['q'].strip().rstrip('.')
    cands = by_q.get(key)
    if not cands:
        miss += 1; continue
    k = used.get(key, 0); q = cands[min(k, len(cands) - 1)]; used[key] = k + 1
    it['tr'], it['sp'], it['tb'], it['pk'] = q['traduzione'], q['spiegazione'], q['trabocchetto'], q['parole_chiave']
    n += 1
h = h[:s] + json.dumps(arr, ensure_ascii=False) + h[s + length:]
open(f, 'w', encoding='utf-8').write(h)
print('updated', n, 'missing', miss)
