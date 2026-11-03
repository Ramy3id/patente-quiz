import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderGlobalFooter')
end_idx = text.find('function initUnifiedNav', idx)
if end_idx == -1:
    end_idx = idx + 4000
print(text[idx:end_idx])
