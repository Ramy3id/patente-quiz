import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('Zero Horizontal Scroll & No Cutoff')
if idx != -1:
    print(content[idx-50:idx+600])
else:
    print("Comment not found, searching for .filter-chips")
    idx = content.find('.filter-chips {')
    while idx != -1:
        print(content[idx-20:idx+250])
        print("----")
        idx = content.find('.filter-chips {', idx+1)
