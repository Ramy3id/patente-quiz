import json
base = r'Capitoli_Divisi/Capitolo_08_segnali_indicazione/'
html = open(base + 'index.html', encoding='utf-8').read()
new = json.load(open(base + 'domande.json', encoding='utf-8'))
marker = 'const DATA = '
s = html.index(marker) + len(marker)
old, length = json.JSONDecoder().raw_decode(html[s:])
assert len(old['domande']) == len(new['domande']) == 603
html = html[:s] + json.dumps(new, ensure_ascii=False) + html[s + length:]
open(base + 'index.html', 'w', encoding='utf-8').write(html)
print('filler left:', html.count('سؤال يتناول'))
print('new present:', sum(1 for q in new['domande'] if q['spiegazione'][:40] in html), '/ 603')
