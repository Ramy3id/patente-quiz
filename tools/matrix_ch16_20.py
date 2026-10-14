import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

chapters = [
    (16, 'interactive_pages/دليل_الباب_16_الوقوف_والتوقف_والركن.html'),
    (17, 'interactive_pages/دليل_الباب_17_الأوتوستراد_والحمولة_وسحب_المقطورات.html'),
    (18, 'interactive_pages/دليل_الباب_18_استخدام_الأضواء_ولمبات_التابلوه_والعواكس.html'),
    (19, 'interactive_pages/دليل_الباب_19_أحزمة_الأمان_والخوذة_ومقاعد_الأطفال.html'),
    (20, 'interactive_pages/دليل_الباب_20_رخص_القيادة_والنقاط_والعقوبات.html'),
]

for ch, path in chapters:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    has_studio = 'studio' in html.lower()
    has_gallery = 'gallery' in html.lower() or 'معرض' in html
    trap_quiz_count = len(re.findall(r'class=["\']trap-quiz-text["\']', html))
    img_count = len(re.findall(r'<img\b', html))
    cards_count = len(re.findall(r'class=["\']technical-card["\']', html))
    hero_badges = len(re.findall(r'class=["\']hero-stat-badge["\']', html))
    
    print(f"Chapter {ch}:")
    print(f"   Studio: {has_studio} | Gallery: {has_gallery} | Trap Quiz Cards: {trap_quiz_count}")
    print(f"   Technical Cards: {cards_count} | Images: {img_count} | Hero Badges: {hero_badges}")
