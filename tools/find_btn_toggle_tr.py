with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('btnToggleTr')
idx2 = html.find('btnToggleTr', idx + 20)
idx3 = html.find('btnToggleTr', idx2 + 20)
print(html[idx3-50:idx3+400])
