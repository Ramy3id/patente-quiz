import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect media queries in allenamento-capitolo.html
import re
mqs = re.findall(r'@media[^{]*\{[\s\S]*?\}\s*\}', content)
print(f"Found {len(mqs)} media queries")
for m in mqs:
    if 'choice' in m or 'vf' in m or 'grid' in m or 'button' in m or 'card' in m or 'footer' in m:
        print("MATCHING MQ:")
        print(m[:400])
        print("="*40)
