import os
import re

base_dir = r"R:\Ramy\PATENTE\Capitoli_Divisi"
base_url = "https://patente-quiz-livid.vercel.app"

chapters = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("Capitolo_")]
chapters.sort()

count = 0
for ch in chapters:
    index_path = os.path.join(base_dir, ch, "index.html")
    if not os.path.exists(index_path):
        continue
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if already has canonical
    if '<link rel="canonical"' in content:
        continue
    
    # Extract title
    title_match = re.search(r"<title>(.*?)</title>", content)
    title_text = title_match.group(1) if title_match else ch
    title_clean = title_text.replace('"', '&quot;')
    
    canonical_url = f"{base_url}/Capitoli_Divisi/{ch}/index.html"
    
    seo_block = f'''<link rel="canonical" href="{canonical_url}">
<link rel="alternate" hreflang="ar" href="{canonical_url}">
<link rel="alternate" hreflang="it" href="{canonical_url}">
<link rel="alternate" hreflang="x-default" href="{canonical_url}">
<meta name="description" content="شرح وكويزات رخصة القيادة الإيطالية Patente B - {title_clean} بالعربي والإيطالي مع فخوخ الأسئلة وشرح الكلمات المفتاحية.">

<!-- Breadcrumb Schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "الرئيسية", "item": "{base_url}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "فهرس الأبواب", "item": "{base_url}/Capitoli_Divisi/index.html" }},
    {{ "@type": "ListItem", "position": 3, "name": "{title_clean}", "item": "{canonical_url}" }}
  ]
}}
</script>'''

    # Insert after <title>...</title>
    if title_match:
        content = content.replace(title_match.group(0), title_match.group(0) + "\n" + seo_block, 1)
    
    # Upgrade contrast variables
    content = content.replace("--text-muted: #71717a;", "--text-muted: #94a3b8;")
    content = content.replace("--text-secondary: #a1a1aa;", "--text-secondary: #cbd5e1;")
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    count += 1
    print(f"Upgraded Chapter {ch}")

print(f"Successfully upgraded SEO & Contrast across {count} chapters!")
