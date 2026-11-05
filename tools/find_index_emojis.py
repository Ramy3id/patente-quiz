import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all occurrences of emojis in Capitoli_Divisi/index.html
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]')
matches = emoji_pattern.findall(text)
unique = sorted(set(matches))
print("Total emoji occurrences in index.html:", len(matches))
print("Unique emojis:", unique)

# Print lines where they occur
lines = text.split('\n')
for i, line in enumerate(lines):
    found = emoji_pattern.findall(line)
    if found:
        print(f"Line {i+1}: {set(found)} -> {line.strip()[:100]}")
