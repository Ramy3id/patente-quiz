import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect .chips-actions and .segmented-filter-bar in parole-quiz.html
import re
print("--- chips-actions ---")
for m in re.finditer(r'\.chips-actions\s*\{[^}]+\}', text):
    print(m.group(0))

print("--- segmented-filter-bar ---")
for m in re.finditer(r'\.segmented-filter-bar\s*\{[^}]+\}', text):
    print(m.group(0))
