with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[4365:4430]):
    print(f"{i+4366}: {l.strip().encode('ascii', 'backslashreplace').decode('ascii')}")
