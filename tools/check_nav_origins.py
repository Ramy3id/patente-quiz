with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Has #globalPortalNav:", 'globalPortalNav' in text)
print("Has #portal-nav:", 'portal-nav' in text)
print("Has <nav:", '<nav' in text)

# Where does #globalPortalNav come from in Capitoli_Divisi/index.html?
# Let's search unified-nav.js for how globalPortalNav or portal-nav is injected or targeted!
with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("In unified-nav.js:")
print("globalPortalNav count:", js.count('globalPortalNav'))
print("portal-nav count:", js.count('portal-nav'))
