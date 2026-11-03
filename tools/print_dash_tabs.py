import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('.dash-tabs-bar {')
print(content[idx:idx+600])

idx2 = content.find('@media')
while idx2 != -1:
    m = content[idx2:idx2+400]
    if 'dash-tabs-bar' in m:
        print("MQ:")
        print(m[:300])
    idx2 = content.find('@media', idx2+1)
