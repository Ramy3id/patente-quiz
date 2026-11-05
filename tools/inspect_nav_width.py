import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
p = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'class="unified-portal-nav"|#globalPortalNav|\.nav-container|\.main-container|\.ch-portal-container|\.bento-tools-section', text):
    start = max(0, m.start() - 50)
    end = min(len(text), m.end() + 150)
    print(text[start:end])
    print('='*50)
