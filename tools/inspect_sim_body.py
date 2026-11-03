import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect sim-body-grid and controls below the canvas
idx = text.find('sim-body-grid')
print(text[idx-50:idx+2000])
