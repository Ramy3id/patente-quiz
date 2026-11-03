import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 52979
print("--- 600 chars before 52979 ---")
print(text[idx-600:idx])
