# -*- coding: utf-8 -*-
import sys, re, json
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

STOP_WORDS = set('''
il lo la i gli le un uno una di a da in con su per tra fra che e ed o od del dello della dei degli delle
al allo alla ai agli alle dal dallo dalla dai dagli dalle nel nello nella nei negli nelle sul sullo sulla sui
sugli sulle non si se come anche cui piu più quando quale quali questo questa questi queste quello quella
quelli quelle suo sua suoi sue loro ed ha ho hanno sia essere sono era stati stato stata stato stato
figura raffigurata raffigurato segnale posto prima dopo trova presente strada carreggiata veicoli veicolo
obbliga vieta indica prescrive comporta richiede impone
'''.split())

# 1. Sign analysis (Ch 1 - 10)
img_stats = defaultdict(lambda: defaultdict(lambda: {'true': 0, 'false': 0, 'qs': []}))
img_meta = {}

for q in questions:
    if q.get('ch', 0) > 10 or not q.get('img'):
        continue
    img = q['img'].split('/')[-1]
    if img not in img_meta:
        img_meta[img] = {'sub': q.get('sub', ''), 'ch': q.get('ch', 0), 'ch_name': q.get('ch_name', ''), 'full_img': q['img']}
    words = set(re.findall(r'\b[a-zA-Zàèéìòù]{4,}\b', q['q'].lower())) - STOP_WORDS
    ans = q['a']
    for w in words:
        if ans:
            img_stats[img][w]['true'] += 1
        else:
            img_stats[img][w]['false'] += 1
        img_stats[img][w]['qs'].append(q)

sign_rules = []
for img, words in img_stats.items():
    for w, st in words.items():
        tot = st['true'] + st['false']
        if tot >= 3:
            if st['true'] == tot:
                sign_rules.append({'img': img, 'full_img': img_meta[img]['full_img'], 'sub': img_meta[img]['sub'], 'ch': img_meta[img]['ch'], 'word': w, 'type': 'vero', 'count': tot, 'qs': st['qs']})
            elif st['false'] == tot:
                sign_rules.append({'img': img, 'full_img': img_meta[img]['full_img'], 'sub': img_meta[img]['sub'], 'ch': img_meta[img]['ch'], 'word': w, 'type': 'falso', 'count': tot, 'qs': st['qs']})

print(f"Total Sign Rules (min 3 qs, 100% pure): {len(sign_rules)}")
v_signs = [r for r in sign_rules if r['type'] == 'vero']
f_signs = [r for r in sign_rules if r['type'] == 'falso']
print(f" - VERO rules: {len(v_signs)}")
print(f" - FALSO rules: {len(f_signs)}")

# Show top 15 VERO sign rules
print("\n=== TOP 15 SIGN VERO RULES ===")
for r in sorted(v_signs, key=lambda x: x['count'], reverse=True)[:15]:
    print(f"[{r['img']}] {r['sub'][:25]} | Word: '{r['word']}' -> VERO (x{r['count']})")

# Show top 15 FALSO sign rules
print("\n=== TOP 15 SIGN FALSO RULES ===")
for r in sorted(f_signs, key=lambda x: x['count'], reverse=True)[:15]:
    print(f"[{r['img']}] {r['sub'][:25]} | Word: '{r['word']}' -> FALSO (x{r['count']})")

# 2. Theory rules (Ch 11 - 25)
theory_words = defaultdict(lambda: {'true': 0, 'false': 0, 'qs': []})
ch_topic = {
    11: "Limiti e Pericolo (حدود السرعة)",
    12: "Distanza di Sicurezza (مسافة الأمان)",
    13: "Norme Circolazione (قواعد السير والمسارات)",
    14: "Precedenza Incroci (أسبقية التقاطعات)",
    15: "Sorpasso (التجاوز)",
    16: "Fermata e Sosta (الوقوف والتوقف)",
    17: "Autostrade (الطرق السريعة)",
    18: "Luci e Segnali (الأضواء وأجهزة التنبيه)",
    19: "Cinture e Casco (الأحزمة والخوذة)",
    20: "Patente e Punti (الرخص والنقاط)",
    21: "Incidenti Stradali (حوادث السير)",
    22: "Alcool e Primo Soccorso (الكحول والإسعافات)",
    23: "Assicurazione RCA (التأمين والمسؤولية)",
    24: "Consumi e Inquinamento (البيئة والتلوث)",
    25: "Meccanica e Manutenzione (الميكانيكا والصيانة)"
}

theory_stats = defaultdict(lambda: defaultdict(lambda: {'true': 0, 'false': 0, 'qs': []}))
for q in questions:
    ch = q.get('ch', 0)
    if ch < 11:
        continue
    words = set(re.findall(r'\b[a-zA-Zàèéìòù]{4,}\b', q['q'].lower())) - STOP_WORDS
    ans = q['a']
    for w in words:
        if ans:
            theory_stats[ch][w]['true'] += 1
        else:
            theory_stats[ch][w]['false'] += 1
        theory_stats[ch][w]['qs'].append(q)

theory_rules = []
for ch, words in theory_stats.items():
    for w, st in words.items():
        tot = st['true'] + st['false']
        if tot >= 3:
            if st['true'] == tot:
                theory_rules.append({'ch': ch, 'topic': ch_topic.get(ch, ''), 'word': w, 'type': 'vero', 'count': tot, 'qs': st['qs']})
            elif st['false'] == tot:
                theory_rules.append({'ch': ch, 'topic': ch_topic.get(ch, ''), 'word': w, 'type': 'falso', 'count': tot, 'qs': st['qs']})

print(f"\nTotal Chapter-Specific Theory Rules (min 3 qs, 100% pure): {len(theory_rules)}")
v_theory = [r for r in theory_rules if r['type'] == 'vero']
f_theory = [r for r in theory_rules if r['type'] == 'falso']
print(f" - VERO theory rules: {len(v_theory)}")
print(f" - FALSO theory rules: {len(f_theory)}")

# Show top 15 VERO theory rules
print("\n=== TOP 15 THEORY VERO RULES ===")
for r in sorted(v_theory, key=lambda x: x['count'], reverse=True)[:15]:
    print(f"[Cap {r['ch']} - {r['topic']}] Word: '{r['word']}' -> VERO (x{r['count']})")

# Show top 15 FALSO theory rules
print("\n=== TOP 15 THEORY FALSO RULES ===")
for r in sorted(f_theory, key=lambda x: x['count'], reverse=True)[:15]:
    print(f"[Cap {r['ch']} - {r['topic']}] Word: '{r['word']}' -> FALSO (x{r['count']})")
