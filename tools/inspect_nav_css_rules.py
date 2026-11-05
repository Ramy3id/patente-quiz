import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()

# Check hamburger button display rules
idx = nav.find('nav-hamburger')
if idx != -1:
    print("=== nav-hamburger in unified-nav.js ===")
    print(nav[max(0, idx-100):min(len(nav), idx+400)])

# Check native-bottom-dock display rules
idx2 = nav.find('native-bottom-dock')
if idx2 != -1:
    print("=== native-bottom-dock in unified-nav.js ===")
    print(nav[max(0, idx2-100):min(len(nav), idx2+500)])
