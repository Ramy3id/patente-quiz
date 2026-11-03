import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Rebuilt Universal Footer Architecture')
print(text[idx:idx+2500])
