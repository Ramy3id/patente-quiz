import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('repeat(3, minmax(0, 1fr))')
idx = content.find('repeat(3, minmax(0, 1fr))', idx+1)
print("=== second repeat(3) snippet ===")
print(content[max(0, idx-100):min(len(content), idx+500)])
