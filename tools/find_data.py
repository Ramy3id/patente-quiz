import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find('const DATA =')
if pos == -1:
    pos = content.find('DATA =')
print("Position of DATA:", pos)
if pos != -1:
    print(content[pos:pos+500])
