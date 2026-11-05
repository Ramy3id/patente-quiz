import sys

sys.stdout.reconfigure(encoding='utf-8')
p = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace LinkedIn link
text = text.replace('https://linkedin.com/in/ramy-eid-fahmy', 'https://www.linkedin.com/in/ramy-eid-fahmy-dev')
text = text.replace('https://www.linkedin.com/in/ramy-eid-fahmy"', 'https://www.linkedin.com/in/ramy-eid-fahmy-dev"')

with open(p, 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: Updated LinkedIn link in unified-nav.js')
