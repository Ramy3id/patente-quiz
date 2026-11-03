import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = ['فهرس الـ 25', 'Definizioni generali', 'فهرس أجزاء', 'كل الأجزاء', 'المتبقي']
for m in matches:
    idx = text.find(m)
    print(f"Match '{m}': found={idx != -1}")
    if idx != -1:
        print(text[max(0, idx-100):min(len(text), idx+300)])
        print('='*40)
