import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('chapter-search')
while idx != -1:
    print(content[max(0, idx-100):min(len(content), idx+400)])
    print("---------------------------------")
    idx = content.find('chapter-search', idx+1)
