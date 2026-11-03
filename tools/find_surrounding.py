with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('أنت تتصفح كزائر')
with open(r'R:\Ramy\PATENTE_PRO_APP\tools\banner_surrounding.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx-400:idx+600])
print('Saved banner_surrounding.txt')
