import os

base_url = 'https://patente-quiz-livid.vercel.app'
chapters_dir = r'R:\Ramy\PATENTE\Capitoli_Divisi'
chapters = [d for d in os.listdir(chapters_dir) if os.path.isdir(os.path.join(chapters_dir, d)) and d.startswith('Capitolo_')]
chapters.sort()

interactive_dir = r'R:\Ramy\PATENTE\interactive_pages'
interactive_pages = [f for f in os.listdir(interactive_dir) if f.endswith('.html') and f != 'dashboard.html']
interactive_pages.sort()

xml = ['<?xml version="1.0" encoding="UTF-8"?>']
xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')

def add_url(loc, priority='0.8', freq='weekly'):
    xml.append('  <url>')
    xml.append(f'    <loc>{loc}</loc>')
    xml.append(f'    <xhtml:link rel="alternate" hreflang="ar" href="{loc}"/>')
    xml.append(f'    <xhtml:link rel="alternate" hreflang="it" href="{loc}"/>')
    xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>')
    xml.append(f'    <changefreq>{freq}</changefreq>')
    xml.append(f'    <priority>{priority}</priority>')
    xml.append('  </url>')

# Main hubs
add_url(f'{base_url}/Capitoli_Divisi/index.html', '1.0', 'daily')
add_url(f'{base_url}/Simulatore_Esame.html', '0.9', 'daily')
add_url(f'{base_url}/Studio_Quiz_Patente.html', '0.9', 'weekly')

# All 25 chapters
for ch in chapters:
    add_url(f'{base_url}/Capitoli_Divisi/{ch}/index.html', '0.85', 'weekly')

# Interactive study tools
for p in interactive_pages:
    add_url(f'{base_url}/interactive_pages/{p}', '0.7', 'monthly')

xml.append('</urlset>')

with open(r'R:\Ramy\PATENTE\sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml))

print(f'Sitemap created successfully with {len(chapters) + len(interactive_pages) + 3} URLs!')
