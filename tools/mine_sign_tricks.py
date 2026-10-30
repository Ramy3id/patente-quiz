# -*- coding: utf-8 -*-
import sys, os, glob, re, json
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

chapters = sorted(glob.glob('R:/Ramy/PATENTE/Capitoli_Divisi/Capitolo_*/index.html'))
all_questions = []

for ch in chapters:
    with open(ch, 'r', encoding='utf-8') as f:
        text = f.read()
    m = re.search(r'const DATA = ({.*?});\s*const UNIFIED_GROUPS', text, re.DOTALL)
    if not m:
        m = re.search(r'const DATA = ({.*?});', text, re.DOTALL)
    if m:
        try:
            d = json.loads(m.group(1))
            domande = d.get('domande', [])
            all_questions.extend(domande)
        except:
            pass

print(f"Loaded {len(all_questions)} questions from chapters.")

STOP_WORDS = set('''
il lo la i gli le un uno una di a da in con su per tra fra che e ed o od del dello della dei degli delle
al allo alla ai agli alle dal dallo dalla dai dagli dalle nel nello nella nei negli nelle sul sullo sulla sui
sugli sulle non si se come anche cui piu più quando quale quali questo questa questi queste quello quella
quelli quelle suo sua suoi sue loro ed ha ho hanno sia essere sono era stati stato stata stato stato
figura raffigurata raffigurato segnale posto prima dopo
'''.split())

img_word_stats = defaultdict(lambda: defaultdict(lambda: {'true': 0, 'false': 0, 'examples': []}))
img_subtopic = {}

for q in all_questions:
    img = q.get('immagine')
    if not img:
        continue
    img_name = img.split('/')[-1]
    if img_name not in img_subtopic and q.get('sotto_argomento'):
        img_subtopic[img_name] = q.get('sotto_argomento')
        
    ans = q.get('risposta')
    text = q.get('domanda', '').lower()
    words = set(re.findall(r'\b[a-zA-Zàèéìòù]{4,}\b', text)) - STOP_WORDS
    for w in words:
        if ans:
            img_word_stats[img_name][w]['true'] += 1
        else:
            img_word_stats[img_name][w]['false'] += 1
        img_word_stats[img_name][w]['examples'].append((q.get('domanda'), ans))

always_true = []
always_false = []

for img, words in img_word_stats.items():
    for w, st in words.items():
        total = st['true'] + st['false']
        if total >= 3:
            if st['true'] == total:
                always_true.append((img, w, total, img_subtopic.get(img, '')))
            elif st['false'] == total:
                always_false.append((img, w, total, img_subtopic.get(img, '')))

print(f"\nResults of Pair-Mining:")
print(f"Total Sign + Keyword rules with 100% VERO (min 3 questions): {len(always_true)}")
print(f"Total Sign + Keyword rules with 100% FALSO (min 3 questions): {len(always_false)}")

print("\n--- Top 10 Sign + Word rules (100% VERO) ---")
for img, w, cnt, sub in sorted(always_true, key=lambda x: x[2], reverse=True)[:10]:
    print(f"Sign: {img:20} [{sub:30}] | Word: '{w:15}' -> 100% VERO (Count: {cnt})")

print("\n--- Top 10 Sign + Word rules (100% FALSO) ---")
for img, w, cnt, sub in sorted(always_false, key=lambda x: x[2], reverse=True)[:10]:
    print(f"Sign: {img:20} [{sub:30}] | Word: '{w:15}' -> 100% FALSO (Count: {cnt})")
