import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

for mq in ['@media (min-width: 1200px)', '@media (max-width: 992px)', '@media (max-width: 768px)', '@media (min-width: 641px)']:
    idx = nav.find(mq)
    if idx != -1:
        print(f"=== {mq} ===")
        print(nav[idx:idx+400])
        print("--------------------")
