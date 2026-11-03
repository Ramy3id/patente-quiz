with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="searchInput"')
print(html[idx-100:idx+800])
