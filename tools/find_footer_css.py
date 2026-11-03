import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for footer CSS inside unified-nav.js
idx = text.find('.footer-col')
if idx != -1:
    print("Found .footer-col in unified-nav.js at:", idx)
    print(text[idx-200:idx+800])
else:
    print("Not found in unified-nav.js")

# Also search for footer container
idx_f = text.find('id="unifiedFooter"')
if idx_f == -1:
    idx_f = text.find("id=\\\"unifiedFooter\\\"")
print("unifiedFooter tag:", idx_f)
if idx_f != -1:
    print(text[idx_f-50:idx_f+400])
