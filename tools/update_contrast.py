files = [
    r'R:\Ramy\PATENTE\Simulatore_Esame.html',
    r'R:\Ramy\PATENTE\Capitoli_Divisi\index.html'
]

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('--text-muted: #71717a;', '--text-muted: #94a3b8;')
    content = content.replace('--text-secondary: #a1a1aa;', '--text-secondary: #cbd5e1;')
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated text contrast variables to WCAG AAA standards in HTML hubs!")
