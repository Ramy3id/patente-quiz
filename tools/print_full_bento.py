import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_kw = '<!-- الشبكة الرئيسية: أول 4 معامل أساسية تظهر فوراً -->'
if start_kw not in content:
    start_kw = '<!-- الشبكة الرئيسية:'

idx1 = content.find(start_kw)
idx2 = content.find('<!-- زر توسيع / طي باقي المعامل -->')

print("=== Current Bento Section HTML ===")
print(content[idx1:idx2])
