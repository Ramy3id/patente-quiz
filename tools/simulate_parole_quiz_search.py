# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

# Check data_thesaurus.js
with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_thesaurus.js', 'r', encoding='utf-8') as f:
    th_text = f.read()

m_th = re.search(r'const PATENTE_THESAURUS = (\[.*?\]);', th_text, re.DOTALL)
thesaurus = json.loads(m_th.group(1)) if m_th else []

def getItalianStem(word):
    w = word.strip().lower()
    if len(w) <= 4:
        return w
    suffixes = ['amente', 'mente', 'azioni', 'azione', 'aggio', 'abile', 'ibili', 'ando', 'endo', 'ante', 'ente', 'arsi', 'ersi', 'irsi', 'are', 'ere', 'ire', 'ata', 'ato', 'ati', 'ate', 'ivo', 'iva', 'ivi', 'ive']
    for s in suffixes:
        if w.endswith(s) and len(w) - len(s) >= 3:
            return w[:-len(s)]
    if len(w) >= 5 and re.search(r'[aeio]$', w):
        return w[:-1]
    return w

def getSynonymsForWord(word):
    clean = word.lower().strip()
    stem = getItalianStem(clean)
    synonymsSet = set()
    for item in thesaurus:
        baseClean = item['parola_base'].lower()
        baseStem = getItalianStem(baseClean)
        matchBase = (clean in baseClean) or (baseClean in clean) or (baseStem == stem)
        matchSynonym = False
        for s in item.get('sinonimi', []):
            sc = (s['it'] if isinstance(s, dict) else s).lower()
            if (clean in sc) or (sc in clean) or (getItalianStem(sc) == stem):
                matchSynonym = True
                break
        if matchBase or matchSynonym:
            synonymsSet.add(item['parola_base'].lower())
            for s in item.get('sinonimi', []):
                sw = (s['it'] if isinstance(s, dict) else s).lower()
                synonymsSet.add(sw)
    return list(synonymsSet)

# Test with default settings in parole-quiz: useStemming=True, useSynonyms=True
query = "montare"
stem = getItalianStem(query)
syns = getSynonymsForWord(query)
print(f"Query: '{query}', Stem: '{stem}', Synonyms found in Thesaurus: {syns}")

matched_default = []
for q in questions:
    qText = q.get('q', '').lower()
    qTr = q.get('tr', '').lower()
    qSp = q.get('sp', '').lower()
    pk_list = q.get('pk', [])
    qPk = " ".join([p if isinstance(p, str) else p.get('it', '') + ' ' + p.get('ar', '') for p in pk_list]).lower()
    fullDomain = f"{qText} {qTr} {qSp} {qPk}"

    candidates = [query] + syns
    matched = False
    for c in candidates:
        c_stem = getItalianStem(c)
        if (c in fullDomain) or (len(c_stem) >= 3 and c_stem in fullDomain):
            matched = True
            break
    if matched:
        matched_default.append(q)

v_cnt = len([q for q in matched_default if q.get('a')])
f_cnt = len([q for q in matched_default if not q.get('a')])
print(f"\nSimulation with Stemming + Synonyms + FullDomain:")
print(f"Total: {len(matched_default)} | VERO: {v_cnt} | FALSO: {f_cnt}")

# Let's see what happens if someone searched without synonyms or in text only
# Or let's see which specific 15 questions matched in parole-quiz.html!
