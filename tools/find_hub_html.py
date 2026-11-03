import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'subtopics-chips-bar' in l:
        start = max(0, i-20)
        end = min(len(lines), i+30)
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}", end="")
        break
