import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/theme-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- theme-engine.js ---")
print(text[:1500])
