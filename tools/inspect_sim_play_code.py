import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('sim-action-btns')
if idx != -1:
    print(text[idx-50:idx+800])
else:
    idx2 = text.find('btnPlaySim')
    print("btnPlaySim at", idx2)
    print(text[idx2-100:idx2+600])
