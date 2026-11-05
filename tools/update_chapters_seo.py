import os, sys, glob, re

sys.stdout.reconfigure(encoding='utf-8')

repo = r'R:\Ramy\PATENTE_PRO_APP'

chapter_files = glob.glob(repo + r'\Capitoli_Divisi\Capitolo_*\index.html')
print(f"Found {len(chapter_files)} chapter index.html files")

total_vercel_found = 0
for ch in chapter_files:
    with open(ch, 'r', encoding='utf-8') as f:
        c = f.read()
    cnt = c.count('https://patente-quiz-livid.vercel.app')
    if cnt > 0:
        total_vercel_found += cnt
        c = c.replace('https://patente-quiz-livid.vercel.app', 'https://ramy3id.github.io/patente-quiz')
        # Also add opensearch link if missing
        if 'opensearch.xml' not in c:
            idx = c.find('</head>')
            if idx != -1:
                c = c[:idx] + '\n<link rel="search" type="application/opensearchdescription+xml" title="البحث في كويزات الباتنتى — Patente B Pro" href="../../opensearch.xml">\n' + c[idx:]
        with open(ch, 'w', encoding='utf-8') as f:
            f.write(c)

print(f"Replaced {total_vercel_found} occurrences of old Vercel URL across chapter files and added OpenSearch links!")
