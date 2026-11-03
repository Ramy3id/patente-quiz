import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('renderHub()')
if idx != -1:
    print(content[idx:idx+2500])
