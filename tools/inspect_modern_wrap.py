with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="modernScreenWrap"')
print(html[idx:idx+600])
