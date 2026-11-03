import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

cards = re.findall(r'<div class="chapter-card"[^>]*data-cat="([^"]+)"', c)
print(f"Total cards found: {len(cards)}")
from collections import Counter
print("Categories in cards:", Counter(cards))
