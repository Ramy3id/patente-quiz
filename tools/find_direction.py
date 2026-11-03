import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

for m in re.finditer(r'dir\s*=\s*["\'][^"\']*["\']', content):
    pos = m.start()
    print(content[max(0, pos-30):min(len(content), pos+60)])

for line in content.splitlines():
    if 'text-align' in line or 'direction' in line:
        print("CSS:", line.strip())
