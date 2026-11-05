import sys, re

sys.stdout.reconfigure(encoding='utf-8')

repo = r'R:\Ramy\PATENTE_PRO_APP'

seo_configs = {
    r'interactive_pages\scheda-esame.html': {
        'title': 'محاكي الامتحان الوزاري الرسمي (30 سؤال / 20 دقيقة) | Patente B Pro 2026',
        'desc': 'محاكي الامتحان التجريبي الرسمي لرخصة القيادة الإيطالية Patente B لعام 2026. 30 سؤالاً في 20 دقيقة، حساب الأخطاء الوزارية الفعلي، الشرح الصوتي، والترجمة التفاعلية بالعربي والإيطالي.',
        'keywords': 'محاكي امتحان الباتنتى, simulazione esame patente b, quiz patente b 30 domande, امتحان رخصة القيادة الإيطالية, scheda ministeriale patente, كويزات باتنتى بالعربي',
        'canonical': 'https://ramy3id.github.io/patente-quiz/interactive_pages/scheda-esame.html',
        'schema_type': 'Quiz',
        'rel_opensearch': '../opensearch.xml'
    },
    r'interactive_pages\piano-studio.html': {
        'title': 'خطة المذاكرة الذكية وجدول الاستعداد للامتحان | Patente B Pro 2026',
        'desc': 'خطة دراسية ذكية مخصصة لإنهاء منهج رخصة القيادة الإيطالية Patente B في 15 أو 30 أو 45 يوماً. المسار العنقودي الذكي وجدول إتقان الأبواب الـ 25 مع التوزيع المتوازن للأسئلة.',
        'keywords': 'خطة دراسة الباتنتى, piano di studio patente b, جدول مذاكرة رخصة القيادة الايطالية, خطة 30 يوم باتنتى, تعلم الباتنتى بالعربي',
        'canonical': 'https://ramy3id.github.io/patente-quiz/interactive_pages/piano-studio.html',
        'schema_type': 'EducationalOccupationalProgram',
        'rel_opensearch': '../opensearch.xml'
    },
    r'Capitoli_Divisi\parole-quiz.html': {
        'title': 'بنك كلماتي ومستكشف الفخاخ في الأسئلة الوزارية | Patente B Pro 2026',
        'desc': 'قاموس المصطلحات والمترادفات الوزارية لرخصة القيادة الإيطالية بالعربي والإيطالي. فلترة الكلمات الأكثر تكراراً، كشف الفروق الخادعة (Falsi Sinonimi)، وجذور الكلمات الوزارية.',
        'keywords': 'كلمات الباتنتى الايطالية, parole patente b arabo, مصطلحات رخصة القيادة الايطالية مترجمة, فخاخ الباتنتى, قاموس باتنتى عربي ايطالي',
        'canonical': 'https://ramy3id.github.io/patente-quiz/Capitoli_Divisi/parole-quiz.html',
        'schema_type': 'LearningResource',
        'rel_opensearch': '../opensearch.xml'
    },
    r'interactive_pages\cerca-quiz.html': {
        'title': 'محرك البحث الوزاري الفوري في الـ 7,139 سؤالاً | Patente B Pro 2026',
        'desc': 'ابحث لحظياً بالصوت أو النص في جميع أسئلة رخصة القيادة الإيطالية Patente B الوزارية المعتمدة بالعربي والإيطالي مع كشف الفخاخ، الشرح المعتمد، والإحصائيات الرسمية.',
        'keywords': 'بحث في اسئلة الباتنتى, cerca quiz patente b, محرك بحث كويزات رخصة القيادة, اسئلة الباتنتى مترجمة, بحث صوتي باتنتى',
        'canonical': 'https://ramy3id.github.io/patente-quiz/interactive_pages/cerca-quiz.html',
        'schema_type': 'SearchAction',
        'rel_opensearch': '../opensearch.xml'
    }
}

for rel_path, cfg in seo_configs.items():
    full_path = repo + '\\' + rel_path
    with open(full_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace old Vercel links
    html = html.replace('https://patente-quiz-livid.vercel.app', 'https://ramy3id.github.io/patente-quiz')
    
    # Build complete SEO block
    seo_block = f'''
  <!-- Primary Meta Tags -->
  <meta name="description" content="{cfg['desc']}">
  <meta name="keywords" content="{cfg['keywords']}">
  <link rel="canonical" href="{cfg['canonical']}">
  <link rel="alternate" hreflang="ar" href="{cfg['canonical']}">
  <link rel="alternate" hreflang="it" href="{cfg['canonical']}">
  <link rel="alternate" hreflang="x-default" href="{cfg['canonical']}">

  <!-- OpenSearch Integration for Browser Omnibox -->
  <link rel="search" type="application/opensearchdescription+xml" title="البحث في كويزات الباتنتى — Patente B Pro" href="{cfg['rel_opensearch']}">

  <!-- Open Graph / Facebook / WhatsApp / Telegram -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{cfg['canonical']}">
  <meta property="og:title" content="{cfg['title']}">
  <meta property="og:description" content="{cfg['desc']}">
  <meta property="og:image" content="https://ramy3id.github.io/patente-quiz/assets/icons/icon-512.png">
  <meta property="og:image:width" content="512">
  <meta property="og:image:height" content="512">
  <meta property="og:site_name" content="Patente B Pro">
  <meta property="og:locale" content="ar_AR">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="{cfg['canonical']}">
  <meta name="twitter:title" content="{cfg['title']}">
  <meta name="twitter:description" content="{cfg['desc']}">
  <meta name="twitter:image" content="https://ramy3id.github.io/patente-quiz/assets/icons/icon-512.png">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "{cfg['schema_type']}",
    "name": "{cfg['title']}",
    "description": "{cfg['desc']}",
    "url": "{cfg['canonical']}",
    "inLanguage": ["ar", "it"],
    "provider": {{
      "@type": "EducationalOrganization",
      "name": "Patente B Pro",
      "url": "https://ramy3id.github.io/patente-quiz/"
    }}
  }}
  </script>
'''
    # Update title
    title_pattern = r'<title>.*?</title>'
    new_title_tag = f"<title>{cfg['title']}</title>"
    if re.search(title_pattern, html, re.I):
        html = re.sub(title_pattern, new_title_tag, html, count=1, flags=re.I)
    
    # Remove any existing canonical or opensearch or og:url in head to avoid duplicates
    html = re.sub(r'<link\s+rel=["\']canonical["\'].*?>', '', html, flags=re.I)
    html = re.sub(r'<link\s+rel=["\']search["\'].*?>', '', html, flags=re.I)
    
    # Insert seo_block right after title tag
    idx_title = html.find('</title>')
    if idx_title != -1:
        insert_pos = idx_title + len('</title>')
        html = html[:insert_pos] + seo_block + html[insert_pos:]
    else:
        idx_head = html.find('<head>')
        if idx_head != -1:
            insert_pos = idx_head + len('<head>')
            html = html[:insert_pos] + seo_block + html[insert_pos:]
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Injected comprehensive SEO & OpenSearch into {rel_path} successfully!")

print("\nAll 4 core interactive tools updated successfully!")
