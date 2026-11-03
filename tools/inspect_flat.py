import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("currentViewMode === 'flat'")
if idx == -1:
    idx = content.find("mode === 'flat'")
if idx != -1:
    print(content[idx-50:idx+500])
else:
    # search flat
    for line in content.splitlines():
        if 'flat' in line:
            print("FLAT:", line)
