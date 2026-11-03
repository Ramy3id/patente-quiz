import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('المنظومة الرقمية')
print("Found 'المنظومة الرقمية' at index:", idx)
print(text[idx-500:idx+1500])
