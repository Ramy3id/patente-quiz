import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

for ch in range(20, 26):
    fname = None
    for f in os.listdir('interactive_pages'):
        if f.startswith(f"دليل_الباب_{ch}_") and f.endswith('.html'):
            fname = os.path.join('interactive_pages', f)
            break
    if not fname:
        print(f"Ch {ch}: Not found")
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as fp:
        html = fp.read()
    studio = 'studio' in html.lower()
    gallery = 'gallery' in html.lower() or 'معرض' in html
    traps = len(re.findall(r'class=["\']trap-quiz-text["\']', html))
    signal_cards = len(re.findall(r'class=["\']signal-card["\']', html))
    tech_cards = len(re.findall(r'class=["\']technical-card["\']', html))
    imgs = len(re.findall(r'<img\b', html))
    print(f"Chapter {ch} ({os.path.basename(fname)}):")
    print(f"   Studio: {studio} | Gallery: {gallery} | Traps: {traps}")
    print(f"   Cards: signal={signal_cards}, tech={tech_cards} | Images: {imgs}")
