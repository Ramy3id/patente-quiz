import sys, json, time, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = 'PatenteDidattica/1.0 (https://patente-quiz.it; info@patente-quiz.it) Python-urllib'

def get_category_images(category, limit=10):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=categorymembers&gcmtitle=Category:{urllib.parse.quote(category)}&gcmtype=file&gcmlimit={limit}&prop=imageinfo&iiprop=url|size|mime"
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            res = []
            for k, v in pages.items():
                title = v.get('title', '')
                ii = v.get('imageinfo', [{}])[0]
                url_img = ii.get('url', '')
                mime = ii.get('mime', '')
                size = ii.get('size', 0)
                if 'jpg' in mime or 'jpeg' in mime or 'png' in mime:
                    res.append({'title': title, 'url': url_img, 'size': size})
            return res
    except Exception as e:
        print(f"Error for {category}: {e}")
        return []

cats = [
    'Breathalyzers',
    'Recovery position',
    'First aid',
    'Splints',
    'Space blankets',
    'Hazard warning triangles',
    'High-visibility clothing',
    'Motorcycle helmets',
    'Emergency medical services in Italy',
    'Drug testing'
]

results = {}
for c in cats:
    imgs = get_category_images(c, 8)
    results[c] = imgs
    print(f"Cat: {c:35} -> {len(imgs)} files: {[i['title'][:35] for i in imgs[:3]]}")
    time.sleep(1.0)

with open('category_images.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
