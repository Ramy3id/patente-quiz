import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('.bento-toggle-btn')
if idx != -1:
    print("=== CSS ===")
    print(text[idx:idx+800])

idx_js = text.find('toggleBentoExtraTools')
if idx_js != -1:
    print("=== JS ===")
    print(text[idx_js-50:idx_js+600])
