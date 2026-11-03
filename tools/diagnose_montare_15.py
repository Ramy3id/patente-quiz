# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

# Check parole-quiz.html search logic with different options
# Possibility 1: Did the user search for "montare" with chapter filter?
for ch in range(1, 26):
    q_ch = [q for q in questions if q['ch'] == ch]
    m_ch = [q for q in q_ch if 'mont' in q['q'].lower()]
    v = len([q for q in m_ch if q['a']])
    f = len([q for q in m_ch if not q['a']])
    if len(m_ch) == 15 and v == 14 and f == 1:
        print(f"Match in chapter {ch}: 15 qs, 14 V, 1 F")

# Possibility 2: Did the search in parole-quiz check q.q, q.tr, q.sp, q.pk?
# Let's search with various substrings of "mont..." across all fields
for term in ["montare", "monta", "montano", "mont", "montato", "montati", "montaggio", "smontare"]:
    res_text = [q for q in questions if term in q['q'].lower()]
    v1 = len([q for q in res_text if q['a']])
    f1 = len([q for q in res_text if not q['a']])
    
    res_all = [q for q in questions if term in (q['q'] + ' ' + q.get('tr','') + ' ' + q.get('sp','')).lower()]
    v2 = len([q for q in res_all if q['a']])
    f2 = len([q for q in res_all if not q['a']])

    print(f"Term: '{term}': in q.q -> {len(res_text)} (V:{v1}, F:{f1}) | in all -> {len(res_all)} (V:{v2}, F:{f2})")

# Possibility 3: What words in the entire DB have EXACTLY 15 questions, with 14 VERO and 1 FALSO?
# Let's tokenize all words in the DB and check which word has total 15 with 14 V and 1 F!
print("\n--- Finding ALL words in the entire Patente database with 15 questions (14 VERO, 1 FALSO) ---")
from collections import defaultdict
word_stats = defaultdict(lambda: {'true': 0, 'false': 0, 'qs': []})
for q in questions:
    words = set(re.findall(r'\b[a-zA-Zàèéìòù]{4,}\b', q['q'].lower()))
    for w in words:
        if q['a']:
            word_stats[w]['true'] += 1
        else:
            word_stats[w]['false'] += 1

matches_15 = []
for w, st in word_stats.items():
    tot = st['true'] + st['false']
    if tot == 15 and st['true'] == 14 and st['false'] == 1:
        matches_15.append(w)

print("Words with exactly 15 questions (14 VERO, 1 FALSO):", matches_15)

# Also check words with total in [14, 15, 16] and F == 1
close_1 = []
for w, st in word_stats.items():
    tot = st['true'] + st['false']
    if tot in [14, 15, 16] and st['false'] == 1:
        close_1.append((w, tot, st['true'], st['false']))
print("\nWords with 14-16 questions and 1 FALSO:", close_1)
