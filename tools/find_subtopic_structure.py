import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in Cap 01: {len(lines)}")
for i, l in enumerate(lines):
    if any(k in l for k in ['فهرس أجزاء', 'subtopic', 'sub-topic', '11 قسم', 'قوائم مقسمة', 'data-section', 'section-body']):
        print(f"{i+1}: {l.strip()[:100]}")
