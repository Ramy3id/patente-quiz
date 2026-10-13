import sys, json, time, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = 'PatenteDidattica/1.0 (https://patente-quiz.it; info@patente-quiz.it) Python-urllib'

def search(q):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrsearch={urllib.parse.quote(q)}&gsrlimit=3&prop=imageinfo&iiprop=url|size|mime"
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            return [{'title': v.get('title'), 'url': v.get('imageinfo', [{}])[0].get('url')} for k, v in pages.items()]
    except Exception as e:
        return []

tests = {
    'triangle': 'warning triangle vehicle',
    'ambulance': 'Croce Rossa ambulanza',
    'recovery_pos': 'recovery position first aid',
    'burns': 'burn treatment cold water',
    'burns_alt': 'burn first aid',
    'vest': 'high-visibility vest car',
    'reaction': 'emergency braking car',
    'drugs': 'drug test panel',
    'alcohol_limits': 'blood alcohol level test',
    'first_aid_scene': 'car crash first aid simulation'
}

for k, q in tests.items():
    res = search(q)
    print(f"{k:18} -> {[r['title'] for r in res]}")
    time.sleep(1.0)
