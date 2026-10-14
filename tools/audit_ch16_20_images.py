import re, os, glob, sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

for ch in [16, 17, 18, 19, 20]:
    matches = glob.glob(f'interactive_pages/*{ch}*.html')
    if not matches:
        continue
    fn = matches[0]
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    imgs = list(dict.fromkeys(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', c)))
    print(f"=== CH {ch} ({len(imgs)} unique images) ===")
    for src in imgs:
        p = os.path.normpath(os.path.join('interactive_pages', src))
        if os.path.exists(p):
            with Image.open(p) as im:
                print(f"   {src} -> {im.size} ({os.path.getsize(p)//1024} KB)")
        else:
            print(f"   MISSING: {src}")
