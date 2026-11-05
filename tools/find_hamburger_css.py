import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

idx = nav.find('.nav-hamburger-btn')
if idx != -1:
    print(nav[max(0, idx-50):min(len(nav), idx+600)])
