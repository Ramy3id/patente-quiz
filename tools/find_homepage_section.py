import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Search for keywords
for kw in ['المعامل', 'الأدوات الذكية', 'الادوات الذكية', 'خطة ال30', '30 يوم']:
    idx = idx_content.find(kw)
    print(f"Keyword '{kw}' in index.html: {idx}")
    if idx != -1:
        print(idx_content[max(0, idx-100):min(len(idx_content), idx+300)])
        print("-------------------")
