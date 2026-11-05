import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

count = content.count('https://patente-quiz-livid.vercel.app')
print(f"Found {count} occurrences of old Vercel URL in Capitoli_Divisi/index.html")

content = content.replace('https://patente-quiz-livid.vercel.app', 'https://ramy3id.github.io/patente-quiz')

# Add OpenSearch link and twitter tags if missing
if 'opensearch.xml' not in content:
    idx = content.find('</head>')
    new_tags = '''<!-- Browser Search Bar Integration (OpenSearch) -->
<link rel="search" type="application/opensearchdescription+xml" title="البحث في كويزات الباتنتى — Patente B Pro" href="../opensearch.xml">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="فهرس أبواب رخصة القيادة الإيطالية 2026 بالعربي والإيطالي — Patente B Pro">
<meta name="twitter:description" content="المنصة الأولى الشاملة لشرح كويزات رخصة القيادة الإيطالية Patente B بالعربي والإيطالي. تغطية الـ 25 باباً، كشف الفخاخ، الشرح الصوتي، ومحاكي الامتحان الوزاري.">
<meta name="twitter:image" content="https://ramy3id.github.io/patente-quiz/assets/icons/icon-512.png">
'''
    content = content[:idx] + new_tags + content[idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Capitoli_Divisi/index.html SEO successfully!")
