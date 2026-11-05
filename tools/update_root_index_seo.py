import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('https://patente-quiz-livid.vercel.app', 'https://ramy3id.github.io/patente-quiz')

# Add opensearch link and twitter tags if not present
if 'opensearch.xml' not in content:
    idx = content.find('</head>')
    new_head_tags = '''<!-- Browser Search Bar Integration (OpenSearch) -->
<link rel="search" type="application/opensearchdescription+xml" title="البحث في كويزات الباتنتى — Patente B Pro" href="opensearch.xml">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="منظومة رخصة القيادة الإيطالية الشاملة 2026 — Patente B Pro">
<meta name="twitter:description" content="تعلم واجتز رخصة القيادة الإيطالية مع الشرح الصوتي، كشف الفخاخ، محاكي الامتحان الوزاري، والترجمة الاحترافية بالعربي والإيطالي.">
<meta name="twitter:image" content="https://ramy3id.github.io/patente-quiz/assets/icons/icon-512.png">

<!-- Google Sitelinks Searchbox Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Patente B Pro",
  "alternateName": "رخصة القيادة الإيطالية بالعربي",
  "url": "https://ramy3id.github.io/patente-quiz/",
  "inLanguage": ["ar", "it"],
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://ramy3id.github.io/patente-quiz/interactive_pages/cerca-quiz.html?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
</script>
'''
    content = content[:idx] + new_head_tags + content[idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated root index.html with official URLs, OpenSearch, Twitter, and Schema.org Sitelinks Searchbox!")
