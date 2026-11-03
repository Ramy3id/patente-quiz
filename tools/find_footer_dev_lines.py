with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
for i, l in enumerate(lines):
    if 'footer-dev' in l or 'dev-icon-btn' in l:
        print(f"{i+1}: {l.strip()}")
