# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

# Check Stop signal
stop_qs = [q for q in questions if q.get('sub') == 'Segnale stop']
print(f"Stop questions: {len(stop_qs)}")
for q in stop_qs[:3]:
    print(" -", q['a'], "|", q['q'])

# Check Discesa pericolosa
discesa_qs = [q for q in questions if 'Discesa pericolosa' in q.get('sub', '')]
print(f"\nDiscesa questions: {len(discesa_qs)}")
for q in discesa_qs[:3]:
    print(" -", q['a'], "|", q['q'])

# Check Primo soccorso questions
soccorso_qs = [q for q in questions if q.get('ch') == 22]
print(f"\nCh 22 questions: {len(soccorso_qs)}")
bere_qs = [q for q in soccorso_qs if re.search(r'\b(bere|bevande|acqua|alcol)\b', q['q'], re.I)]
print(f"Bere/acqua in Ch 22: {len(bere_qs)} qs")
for q in bere_qs[:3]:
    print(" -", q['a'], "|", q['q'])
