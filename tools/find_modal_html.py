with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'fig-modal-close' in line and '<button' in line:
        print(f"Line {i+1}: {line.strip().encode('ascii', 'replace').decode('ascii')}")
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"  {j+1}: {lines[j].strip().encode('ascii', 'replace').decode('ascii')}")
