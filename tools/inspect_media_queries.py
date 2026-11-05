import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

# Search for media queries in unified-nav.js
import re
for m in re.finditer(r'@media[^{]*\{', nav):
    print(m.group(0))
