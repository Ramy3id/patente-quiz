import sys

sys.stdout.reconfigure(encoding='utf-8')
p = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace WhatsApp link
text = text.replace('https://wa.me/393278788484', 'https://wa.me/393447044605')

# Replace Email link
text = text.replace('mailto:ramy.eid.fahmy@gmail.com', 'mailto:ramyeid2311@gmail.com')

with open(p, 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: Updated WhatsApp and Email in unified-nav.js')
