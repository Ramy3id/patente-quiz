import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

print("parole-quiz length:", len(parole))

# Search for the buttons and tags in parole-quiz
for kw in ['تحديد الكل', 'FALSO', 'Stemming', 'Velocità']:
    idx = parole.find(kw)
    print(f"Keyword '{kw}' found at {idx}")
    if idx != -1:
        start = max(0, idx - 200)
        end = min(len(parole), idx + 300)
        print(f"--- Context for {kw} ---")
        print(parole[start:end])
        print("------------------------")
