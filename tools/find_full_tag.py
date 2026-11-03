with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('أنت تتصفح كزائر')
start_div = text.rfind('<div id="guestSyncBanner"', 0, idx)
if start_div == -1:
    start_div = text.rfind('<div', 0, idx - 100)

with open(r'R:\Ramy\PATENTE_PRO_APP\tools\banner_full_tag.txt', 'w', encoding='utf-8') as out:
    out.write(text[start_div:idx+400])
print('Saved banner_full_tag.txt')
