import re, os, sys
from PIL import Image

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
    (25, 'interactive_pages/دليل_الباب_25_الميكانيكا_وصيانة_المركبة_وأجهزة_الأمان.html'),
]

for ch_num, path in chapters:
    if not os.path.exists(path):
        print(f"Missing chapter file: {path}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    img_srcs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content)
    print(f"\n=======================================================")
    print(f"Chapter {ch_num}: {len(img_srcs)} images found in HTML")
    print(f"=======================================================")
    
    unique_srcs = list(dict.fromkeys(img_srcs))
    for src in unique_srcs:
        # resolve relative to interactive_pages
        if src.startswith('../'):
            full_path = os.path.normpath(os.path.join('interactive_pages', src))
        elif src.startswith('http'):
            print(f"   [REMOTE] {src}")
            continue
        else:
            full_path = os.path.normpath(os.path.join('interactive_pages', src))
            
        if os.path.exists(full_path):
            sz = os.path.getsize(full_path)
            try:
                with Image.open(full_path) as im:
                    w, h = im.size
                    fmt = im.format
                    print(f"   [OK] {src} -> {fmt} {w}x{h} ({sz//1024} KB)")
            except Exception as e:
                print(f"   [CORRUPT] {src} ({e})")
        else:
            print(f"   [MISSING] {src} -> {full_path}")
