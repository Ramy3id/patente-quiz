import os
import re

root_dir = r'R:\Ramy\PATENTE_PRO_APP'

# Check Capitolo 01 .container definition
cap01_path = os.path.join(root_dir, r'Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html')
with open(cap01_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for m in re.finditer(r'(\.container\s*\{[^}]*\})', text):
    print("Capitolo 01 .container:", m.group(1).encode('ascii', 'backslashreplace').decode('ascii'))
