import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("File size of modular-chapter-engine.js:", len(content))

# Look for where subtopics / groups are sorted, rendered, or iterated over
for line in content.splitlines():
    if any(k in line.lower() for k in ['unified_groups', 'subtopic', 'groups', 'renderhub', 'rendergrid', 'group']):
        if len(line) < 150:
            print("MATCH:", line)
