with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'<nav[^>]*>[\s\S]*?</nav>', text)
for m in matches[:3]:
    print("Found <nav> in Capitolo 01:")
    print(m[:400].encode('ascii', 'backslashreplace').decode('ascii'))
