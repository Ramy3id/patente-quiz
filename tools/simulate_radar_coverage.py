# -*- coding: utf-8 -*-
import sys, re, json, random
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))
total_bank = len(questions)

# 1. Load MAGIC_WORDS_DB from parole-spia.html
with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'r', encoding='utf-8') as f:
    ps_html = f.read()

# Load RADAR_SIGN_TRAPS and RADAR_THEORY_RULES
with open('R:/Ramy/PATENTE/assets/js/data-radar-expanded.js', 'r', encoding='utf-8') as f:
    r_js = f.read()

m_s = re.search(r'const RADAR_SIGN_TRAPS = (\[.*?\]);', r_js, re.DOTALL)
m_t = re.search(r'const RADAR_THEORY_RULES = (\[.*?\]);', r_js, re.DOTALL)

sign_traps = json.loads(m_s.group(1)) if m_s else []
theory_rules = json.loads(m_t.group(1)) if m_t else []

# Extract MAGIC_WORDS_DB
m_mw = re.search(r'const MAGIC_WORDS_DB = (\[.*?\]);\s*\n\s*/\*\*', ps_html, re.DOTALL)
if not m_mw:
    m_mw = re.search(r'const MAGIC_WORDS_DB = (\[.*?\]);', ps_html, re.DOTALL)

magic_words = json.loads(m_mw.group(1)) if m_mw else []

print(f"Total Questions in DB: {total_bank}")
print(f"Total Magic Words (Tab 1): {len(magic_words)}")
print(f"Total Sign Rules (Tab 2): {len(sign_traps)}")
print(f"Total Theory Rules (Tab 3): {len(theory_rules)}")

# Find questions covered by Tab 1
tab1_qids = set()
for mw in magic_words:
    regex_str = mw.get('regex', '')
    if regex_str:
        try:
            pattern = re.compile(regex_str, re.I)
            for q in questions:
                if pattern.search(q.get('q', '')):
                    tab1_qids.add((q['id'], q['ch']))
        except:
            pass

# Find questions covered by Tab 2
tab2_qids = set()
for r in sign_traps:
    for q in r.get('questions', []):
        tab2_qids.add((q['id'], q['ch']))

# Find questions covered by Tab 3
tab3_qids = set()
for r in theory_rules:
    for q in r.get('questions', []):
        tab3_qids.add((q['id'], q['ch']))

all_radar_qids = tab1_qids | tab2_qids | tab3_qids

print(f"\n--- Coverage Analysis ---")
print(f"Questions covered by Tab 1 (General Magic Words): {len(tab1_qids)}")
print(f"Questions covered by Tab 2 (Sign Traps): {len(tab2_qids)}")
print(f"Questions covered by Tab 3 (Theory Rules): {len(tab3_qids)}")
print(f"Total UNIQUE questions covered across all 3 tabs: {len(all_radar_qids)}")
print(f"Percentage of total bank: {len(all_radar_qids) / total_bank * 100:.2f}%")

# 2. Simulate 10,000 real ministerial exams (Schede d'esame)
# An official exam has 30 questions sampled from the chapters according to ministerial distribution
# In general, 1 or 2 questions from each chapter or group
chapters_dict = defaultdict(list)
for q in questions:
    chapters_dict[q['ch']].append((q['id'], q['ch']))

# Ministerial distribution for 30 questions:
# Chapters 1-10: roughly 14-16 questions
# Chapters 11-20: roughly 10-12 questions
# Chapters 21-25: roughly 3-4 questions
exam_simulations = 10000
hits_per_exam = []

for _ in range(exam_simulations):
    # Pick 30 questions (random sampling across chapters)
    # Most simulators pick 1 from each chapter 1..25, plus 5 extra from large chapters (e.g. 1, 2, 3, 8, 14)
    selected_exam = []
    for ch in range(1, 26):
        if chapters_dict[ch]:
            selected_exam.append(random.choice(chapters_dict[ch]))
    extra_chs = [1, 2, 3, 8, 14]
    for ch in extra_chs:
        selected_exam.append(random.choice(chapters_dict[ch]))
    
    # Count how many are in all_radar_qids
    hit_count = sum(1 for q in selected_exam if q in all_radar_qids)
    hits_per_exam.append(hit_count)

avg_hits = sum(hits_per_exam) / len(hits_per_exam)
min_hits = min(hits_per_exam)
max_hits = max(hits_per_exam)

print(f"\n--- Simulation of 10,000 Real Exams (30 questions each) ---")
print(f"Average questions solved by Radar per exam: {avg_hits:.2f} out of 30 ({avg_hits/30*100:.1f}%)")
print(f"Minimum questions solved in an exam: {min_hits} out of 30")
print(f"Maximum questions solved in an exam: {max_hits} out of 30")

# Frequency distribution
freq = defaultdict(int)
for h in hits_per_exam:
    freq[h] += 1

print("\nFrequency breakdown (Questions solved per 30-question exam):")
for k in sorted(freq.keys()):
    pct = freq[k] / exam_simulations * 100
    bar = '█' * int(pct // 2)
    print(f"  {k:2d} questions: {pct:5.2f}% {bar}")
