import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('جاهز للمحاكاة')
print(text[idx-50:idx+1200])
