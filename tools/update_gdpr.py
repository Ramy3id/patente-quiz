with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    c = f.read()

target = "if (localStorage.getItem('patente_gdpr_consent') === 'accepted') return;"
replacement = "const _c = localStorage.getItem('patente_gdpr_consent'); if (_c === 'accepted' || _c === 'true' || _c === '1') return;"

if target in c:
    c = c.replace(target, replacement)
    with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated GDPR consent check in unified-nav.js successfully")
else:
    print("Target not found")
