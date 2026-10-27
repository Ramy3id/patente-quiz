import os

path = r'R:\Ramy\PATENTE\Capitoli_Divisi\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '<title>فهرس أبواب رخصة القيادة الإيطالية — Patente B Pro</title>'
replacement = '''<title>فهرس أبواب رخصة القيادة الإيطالية بالعربي والإيطالي — Patente B Pro 2026</title>
<meta name="description" content="المنصة الأولى الشاملة لشرح كويزات رخصة القيادة الإيطالية Patente B بالعربي والإيطالي. تغطية الـ 25 باباً، كشف الفخوخ، محاكي الامتحان الوزاري، والمزامنة السحابية.">
<meta name="keywords" content="Quiz patente B in arabo, رخصة القيادة الإيطالية بالعربي, كويزات الباتنتى, اسئلة رخصة القيادة الايطالية مترجمة, امتحان الباتنتى 2026, Quiz ministeriali patente b spiegati in arabo">
<link rel="canonical" href="https://patente-quiz-livid.vercel.app/Capitoli_Divisi/index.html">
<link rel="alternate" hreflang="ar" href="https://patente-quiz-livid.vercel.app/Capitoli_Divisi/index.html">
<link rel="alternate" hreflang="it" href="https://patente-quiz-livid.vercel.app/Capitoli_Divisi/index.html">
<link rel="alternate" hreflang="x-default" href="https://patente-quiz-livid.vercel.app/Capitoli_Divisi/index.html">

<!-- OpenGraph / Social Sharing -->
<meta property="og:type" content="website">
<meta property="og:title" content="منظومة رخصة القيادة الإيطالية الشاملة — Patente B Pro">
<meta property="og:description" content="تعلم واجتز رخصة القيادة الإيطالية مع الشرح الصوتي والفخوخ والترجمة الاحترافية بالعربي والإيطالي.">
<meta property="og:url" content="https://patente-quiz-livid.vercel.app/Capitoli_Divisi/index.html">
<meta property="og:image" content="https://patente-quiz-livid.vercel.app/assets/icons/icon-512.png">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Patente B Pro — رخصة القيادة الإيطالية بالعربي">
<meta name="twitter:description" content="منصة اختبارات وشروحات رخصة القيادة الإيطالية 2026.">
<meta name="twitter:image" content="https://patente-quiz-livid.vercel.app/assets/icons/icon-512.png">

<!-- Google Structured Data (JSON-LD) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "EducationalApplication",
  "name": "Patente B Pro",
  "applicationCategory": "EducationalApplication",
  "operatingSystem": "All",
  "inLanguage": ["ar", "it"],
  "description": "منصة اختبارات وشروحات رخصة القيادة الإيطالية الرسمية مع فخوخ الامتحانات والترجمة التفاعلية.",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "EUR"
  }
}
</script>'''

if target in content:
    content = content.replace(target, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Capitoli_Divisi/index.html SEO tags updated successfully!")
else:
    print("Target title tag not found!")
