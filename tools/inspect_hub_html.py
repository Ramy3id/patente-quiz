with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="examMasterControlHub"')
print(html[idx-100:idx+800])
