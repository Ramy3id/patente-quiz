import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

chapters = [
    (16, 'interactive_pages/دليل_الباب_16_الوقوف_والتوقف_والركن.html'),
    (17, 'interactive_pages/دليل_الباب_17_الأوتوستراد_والحمولة_وسحب_المقطورات.html'),
    (18, 'interactive_pages/دليل_الباب_18_استخدام_الأضواء_ولمبات_التابلوه_والعواكس.html'),
    (19, 'interactive_pages/دليل_الباب_19_أحزمة_الأمان_والخوذة_ومقاعد_الأطفال.html'),
    (20, 'interactive_pages/دليل_الباب_20_رخص_القيادة_والنقاط_والعقوبات.html'),
    (21, 'interactive_pages/دليل_الباب_21_حوادث_السير_وظروف_الطقس_الصعبة.html'),
    (22, 'interactive_pages/دليل_الباب_22_الكحول_والمخدرات_والإسعافات_الأولية.html'),
    (23, 'interactive_pages/دليل_الباب_23_المسؤولية_والتأمين.html'),
    (24, 'interactive_pages/دليل_الباب_24_استهلاك_الوقود_وحماية_البيئة.html'),
    (25, 'interactive_pages/دليل_الباب_25_الميكانيكا_وصيانة_المركبة_وأجهزة_الأمان.html')
]

for ch_num, filename in chapters:
    if not os.path.exists(filename):
        print(f"Ch {ch_num}: FILE MISSING -> {filename}")
        continue
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', c)
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', c)
    has_studio = any('studio' in s.lower() for s in scripts)
    
    print(f"=== Chapter {ch_num} ({os.path.basename(filename)}) ===")
    print(f"   Size: {len(c)} bytes, Lines: {len(c.splitlines())}")
    print(f"   Scripts: {scripts}")
    print(f"   Total images: {len(imgs)}")
    for img in imgs[:4]:
        print(f"     -> {img}")
