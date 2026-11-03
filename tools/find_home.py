import sys
sys.stdout.reconfigure(encoding='utf-8')

for path in [r'R:\Ramy\PATENTE_PRO_APP\index.html', r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
        has_search = 'ابحث باسم الباب' in c
        has_chips = '02-10' in c
        print(f"Path: {path}")
        print(f"  has_search: {has_search}, has_chips: {has_chips}")
        # print title
        import re
        t = re.search(r'<title>(.*?)</title>', c)
        if t: print(f"  Title: {t.group(1)}")
