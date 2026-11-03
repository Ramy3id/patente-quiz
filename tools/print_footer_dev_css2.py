with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('.footer-dev-card-compact')
idx2 = code.find('.footer-dev-card-compact', idx + 30)
print(code[idx2:idx2+1500])
