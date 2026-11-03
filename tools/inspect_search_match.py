# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/parole-quiz.html', 'r', encoding='utf-8') as f:
    text = f.read()

for fn in ['getItalianStem', 'getSynonymsForWord', 'testQuestionMatch', 'onSearchChange']:
    m = re.search(r'function\s+' + fn + r'\b[\s\S]*?(?=function\s+\w+|\Z)', text)
    if m:
        print(f"=== FUNCTION {fn} ===")
        print(m.group(0)[:1200])
        print()
