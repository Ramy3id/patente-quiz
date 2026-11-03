with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('أنت تتصفح كزائر')
print('Found text at:', idx)
start = text.rfind('<div', 0, idx)
start = text.rfind('<div', 0, start) # find outer div
end = text.find('</div>', idx)
end = text.find('</div>', end + 6)
end = text.find('</div>', end + 6)

with open(r'R:\Ramy\PATENTE_PRO_APP\tools\banner_outer_html.txt', 'w', encoding='utf-8') as out:
    out.write(text[start:end+6])
print('Saved banner_outer_html.txt')
