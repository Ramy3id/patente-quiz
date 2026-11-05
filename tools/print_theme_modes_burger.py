import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('.nav-hamburger-btn')
print(c[max(0, idx-50):min(len(c), idx+350)])
