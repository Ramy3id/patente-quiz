import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pos1 = content.find('const UNIFIED_GROUPS = {')
pos2 = content.find('const SUBTOPIC_MAP = {')
print(content[pos1:pos2])
