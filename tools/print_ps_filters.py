with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('class="ps-filters-row"')
print(html[idx:idx+1000])
