# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

for sub in ['Ferito stato shock', 'Ferito ustionato', 'Infortunato fratture agli arti', 'Corpo estraneo occhio']:
    print(f'=== {sub} ===')
    sub_qs = [q for q in questions if q.get('sub') == sub]
    for q in sub_qs:
        ans = "VERO" if q["a"] else "FALSO"
        print(f"[{ans}] {q['q']}")
