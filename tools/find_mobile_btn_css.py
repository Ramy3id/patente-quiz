import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

idx = 0
while True:
    idx = nav.find('nav-mobile-btn', idx)
    if idx == -1: break
    print("Found nav-mobile-btn at", idx)
    print(nav[max(0, idx-50):min(len(nav), idx+300)])
    print("---------------------------------")
    idx += len('nav-mobile-btn')
