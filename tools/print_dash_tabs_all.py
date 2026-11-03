import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('.dash-tabs-bar {', 1000)
while idx != -1:
    print(content[idx-50:idx+300])
    print("="*40)
    idx = content.find('.dash-tabs-bar', idx+1)
