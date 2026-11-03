import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if l.strip().startswith('renderChips()'):
        for j in range(i, min(len(lines), i+90)):
            print(f"{j+1}: {lines[j]}", end="")
        break
