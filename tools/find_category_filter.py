import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('category-filter')
if idx == -1: idx = content.find('filter-pills')
if idx == -1: idx = content.find('الكل')
while idx != -1:
    snippet = content[max(0, idx-100):min(len(content), idx+400)]
    if '25' in snippet and 'باب' in snippet:
        print("=== Found category filter snippet ===")
        print(snippet)
        break
    idx = content.find('الكل', idx+1)
