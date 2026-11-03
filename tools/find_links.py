import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

links = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', content)
for l in links:
    print(l)
