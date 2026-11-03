with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

mIdx = html.find('class="exam-control-hub"')
print('--- HTML MODERN ---')
print(html[mIdx:mIdx + 600])

oIdx = html.find('class="moto-top-header"')
print('--- HTML MOTO ---')
print(html[oIdx:oIdx + 800])
