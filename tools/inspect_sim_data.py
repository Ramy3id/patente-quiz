import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "'608':" in l or '"608":' in l:
        print(f"Line {i+1}:")
        for j in range(i, min(len(lines), i + 45)):
            print(f"  {lines[j].rstrip()}")
        break
