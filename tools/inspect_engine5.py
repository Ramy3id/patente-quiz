import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

for m in re.finditer(r'renderChips\s*\(\)\s*\{', content):
    pos = m.start()
    print("Found renderChips() at", pos)
    print(content[pos:pos+3000])
