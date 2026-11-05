with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'globalPortalNav' in l or 'portal-nav' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
