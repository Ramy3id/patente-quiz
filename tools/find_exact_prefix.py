with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('أنت تتصفح كزائر')
print(ascii(text[idx-700:idx-350]))
