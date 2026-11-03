# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

exact_montare = [q for q in questions if re.search(r'\bmontare\b', q.get('q', ''), re.I)]

print(f"=== EXACT 'montare' (Total: {len(exact_montare)}) ===")
for idx, q in enumerate(exact_montare):
    ans = "VERO" if q["a"] else "FALSO"
    qid = q["id"]
    ch = q["ch"]
    ch_name = q.get("ch_name", "")
    sub = q.get("sub", "")
    print(f"\n#{idx+1} [ID {qid}] [الباب {ch} - {sub}] [{ans}]")
    print(f"IT: {q['q']}")
    print(f"AR: {q.get('tr', '')}")
    print(f"الشرح: {q.get('sp', '')}")

# All verb forms
all_forms = [q for q in questions if re.search(r'\bmont(are|a|ano|i|ato|ata|ati|ate)\b', q.get('q', ''), re.I)]
print(f"\n\n==========================================")
print(f"=== ALL FORMS (Total: {len(all_forms)}) ===")
for idx, q in enumerate(all_forms):
    ans = "VERO" if q["a"] else "FALSO"
    word_m = re.findall(r'\bmont(?:are|a|ano|i|ato|ata|ati|ate)\b', q['q'], re.I)
    print(f"\n#{idx+1} [ID {q['id']}] [الباب {q['ch']} - {q.get('sub', '')}] [{ans}] (Word: {word_m})")
    print(f"IT: {q['q']}")
    print(f"AR: {q.get('tr', '')}")
