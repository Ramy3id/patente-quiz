import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(185, 220):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end="")
