import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'\.bento-toggle-btn\s*\{', text)]
for idx in matches:
    print(text[idx:idx+400])
    print('---')

idx_fn = text.find('function toggleBentoExtraTools')
if idx_fn != -1:
    print("Function:", text[idx_fn:idx_fn+400])
