import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="trafficSimSection"')
end_idx = text.find('</section>', idx)
sec = text[idx:end_idx]

import re
buttons = re.findall(r'<button[^>]*>.*?</button>', sec, re.DOTALL)
print(f"Total buttons in trafficSimSection: {len(buttons)}")
for b in buttons:
    print(b[:120].replace('\n', ' '))
    print('---')
