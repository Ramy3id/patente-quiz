import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

idx = 0
while True:
    idx = nav.find('localStorage', idx)
    if idx == -1:
        break
    print(nav[idx:idx+120].replace('\n', ' '))
    idx += len('localStorage')
