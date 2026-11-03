import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in root index.html: {len(lines)}")
for i in range(min(50, len(lines))):
    print(lines[i].rstrip())
