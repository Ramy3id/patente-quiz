# -*- coding: utf-8 -*-
import sys, re, json
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

# Let's inspect signs and subtopics
signs_by_sub = defaultdict(lambda: {'imgs': set(), 'qs': []})
for q in questions:
    if q.get('ch', 0) <= 10 and q.get('img'):
        sub = q.get('sub', 'Unknown')
        signs_by_sub[sub]['imgs'].add(q['img'])
        signs_by_sub[sub]['qs'].append(q)

print(f"Total subtopics with signs in Ch 1-10: {len(signs_by_sub)}")
for sub, data in sorted(signs_by_sub.items(), key=lambda x: len(x[1]['qs']), reverse=True)[:25]:
    imgs = list(data['imgs'])
    print(f"- {sub[:35]:35} | {len(data['qs'])} qs | Imgs: {imgs[0] if imgs else ''}")
