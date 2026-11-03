import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

for m in re.finditer(r'Object\.keys\s*\(\s*this\.groups\s*\)', content):
    pos = m.start()
    line_start = content.rfind('\n', 0, pos) + 1
    line_end = content.find('\n', pos)
    print(f"Line around {pos}: {content[line_start:line_end].strip()}")
