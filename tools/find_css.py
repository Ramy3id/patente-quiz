import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

# Search all occurrences of chips-actions in CSS
print("=== All CSS with chips-actions ===")
for m in re.finditer(r'([^{}]*chips-actions[^{}]*\{[^{}]*\})', parole):
    print(m.group(0))

print("\n=== All CSS with segmented-filter-bar ===")
for m in re.finditer(r'([^{}]*segmented-filter-bar[^{}]*\{[^{}]*\})', parole):
    print(m.group(0))
