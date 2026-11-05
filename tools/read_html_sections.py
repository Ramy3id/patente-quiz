import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'class="sp-readiness-card"' in l:
        print('=== Readiness Card HTML (lines %d-%d) ===' % (i+1, i+65))
        print(''.join(lines[i:i+65]))
        break
