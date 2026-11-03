import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re

for path in [r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\index.html', r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"=== {path} ===")
    for m in re.finditer(r'btn-toggle|show-more|عرض المزيد|المزيد|إظهار|باقي', text):
        idx = m.start()
        print(text[max(0, idx-60):min(len(text), idx+120)])
        print('---')
