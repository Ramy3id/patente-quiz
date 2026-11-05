import sys

sys.stdout.reconfigure(encoding='utf-8')

for path in [r'R:\Ramy\PATENTE_PRO_APP\index.html', r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"=== {path} ===")
    print("Length:", len(c))
    for term in ['bento-tools-section', 'bento-card', 'المعامل', 'خطة']:
        print(f"  term '{term}':", c.count(term))
