with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('function calculateCounts')
print(html[idx:idx+1500])
