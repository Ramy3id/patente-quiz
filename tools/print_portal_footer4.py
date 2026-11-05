import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

idx = nav.find('مبادرة تعليمية')
if idx != -1:
    print(nav[max(0, idx-200):min(len(nav), idx+400)])
else:
    idx2 = nav.find('Safe Storage')
    print(nav[max(0, idx2-200):min(len(nav), idx2+400)])
