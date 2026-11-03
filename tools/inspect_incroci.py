import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

terms = ['السابق', 'التالي', 'التقاطع الحالي', 'Dinamico Incroci', 'مسار انعطاف طبيعي']
for t in terms:
    idx = text.find(t)
    print(f"Term '{t}': {idx}")
    if idx != -1:
        print(text[max(0, idx-100):min(len(text), idx+300)])
        print("="*40)
