import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.footer-col-title')
if idx != -1:
    print(text[idx-50:idx+1500])
