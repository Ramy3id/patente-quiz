import sys, json, time, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')
USER_AGENT = 'PatenteDidattica/1.0 (https://patente-quiz.it; info@patente-quiz.it) Python-urllib'

def search(q):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrsearch={urllib.parse.quote(q)}&gsrlimit=5&prop=imageinfo&iiprop=url|size|mime"
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            return [{'title': v.get('title'), 'url': v.get('imageinfo', [{}])[0].get('url')} for k, v in pages.items() if 'jpg' in v.get('imageinfo', [{}])[0].get('mime', '') or 'png' in v.get('imageinfo', [{}])[0].get('mime', '')]
    except Exception as e:
        return []

checks = {
    'triangle': 'hazard warning triangle car',
    'tap_water': 'running water tap hand sink',
    'first_aid_cross': 'first aid cross sign kit',
    'skid_mark': 'tire skid marks asphalt road'
}

for k, q in checks.items():
    res = search(q)
    print(f"=== {k} ===")
    for r in res:
        print(f"  {r['title']} -> {r['url']}")
    time.sleep(1.0)
