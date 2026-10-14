import re, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

with open('interactive_pages/دليل_الباب_20_رخص_القيادة_والنقاط_والعقوبات.html', 'r', encoding='utf-8') as f:
    html = f.read()

card_classes = re.findall(r'class=["\']([^"\']*card[^"\']*)["\']', html)
print(Counter(card_classes).most_common(10))
