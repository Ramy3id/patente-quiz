import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    parole = f.read()

# Let's see HTML around تحديد الكل
idx = parole.find('تحديد الكل', 55000)
if idx != -1:
    print("=== HTML around تحديد الكل ===")
    print(parole[idx-300:idx+500])

# Let's see HTML around segmented-filter-bar
idx2 = parole.find('segmented-filter-bar')
if idx2 != -1:
    print("=== HTML/CSS around segmented-filter-bar ===")
    print(parole[idx2-100:idx2+600])

# Let's search for the topic/filter pills like Velocità (or check what pills exist in parole-quiz)
import re
print("=== Search for topic pills / categories ===")
for m in re.finditer(r'<div class="[^"]*tag[^"]*"|<div class="[^"]*chip[^"]*"|<div class="[^"]*topic[^"]*"', parole):
    snippet = parole[m.start():m.start()+200]
    print(snippet)
    break
