import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

# Let's see mobile header HTML inside unified-nav.js
idx = nav.find('nav-mobile-controls')
print("=== nav-mobile-controls HTML snippet ===")
print(nav[max(0, idx-300):min(len(nav), idx+800)])

# Let's see hamburger button CSS
idx2 = nav.find('.nav-hamburger-btn')
print("\n=== .nav-hamburger-btn CSS ===")
print(nav[idx2:idx2+600])
