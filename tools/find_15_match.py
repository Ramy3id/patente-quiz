# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

# Check default words in parole-quiz.html
# Let's inspect parole-quiz.html to see default pre-loaded words / preset packs!
with open('R:/Ramy/PATENTE/Capitoli_Divisi/parole-quiz.html', 'r', encoding='utf-8') as f:
    pq_html = f.read()

# Let's find preset packs in parole-quiz.html
m_packs = re.search(r'const PRESET_PACKS = (\{[\s\S]*?\});', pq_html)
if m_packs:
    print("Found PRESET_PACKS:")
    # print pack names
    packs = re.findall(r'(\w+):\s*\{[\s\S]*?name:\s*[\'"](.*?)[\'"][\s\S]*?words:\s*(\[.*?\])', m_packs.group(1))
    for p in packs:
        print(f"Pack: {p[1]} -> {p[2][:60]}")

# Also check data_thesaurus.js for words with 15 questions (14 V, 1 F)
with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_thesaurus.js', 'r', encoding='utf-8') as f:
    th_text = f.read()

m_th = re.search(r'const PATENTE_THESAURUS = (\[.*?\]);', th_text, re.DOTALL)
thesaurus = json.loads(m_th.group(1)) if m_th else []

print("\n--- Searching Thesaurus for words with ~15 questions (14 V, 1 F) ---")
for item in thesaurus:
    base = item['parola_base']
    # search word in questions
    matched = [q for q in questions if re.search(r'\b' + re.escape(base) + r'\b', q['q'], re.I)]
    v = len([q for q in matched if q['a']])
    f = len([q for q in matched if not q['a']])
    if len(matched) == 15 and v == 14 and f == 1:
        print(f"EXACT MATCH FOUND IN THESAURUS: '{base}' -> Total: 15 (VERO: {v}, FALSO: {f})")
    elif len(matched) in [14, 15, 16] and (v == 14 or v == 13 or v == 15):
        print(f"CLOSE MATCH: '{base}' -> Total: {len(matched)} (VERO: {v}, FALSO: {f})")
