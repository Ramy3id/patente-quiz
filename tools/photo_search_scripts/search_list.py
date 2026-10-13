import urllib.request, urllib.parse, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = 'PatenteDidattica/1.0 (https://patente-quiz.it; info@patente-quiz.it) Python-urllib'

def search(q):
    url = 'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch=' + urllib.parse.quote(q) + '&srnamespace=6&srlimit=5'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            titles = [s['title'] for s in data.get('query', {}).get('search', []) if s['title'].lower().endswith(('.jpg', '.jpeg', '.png'))]
            return titles
    except Exception as e:
        return []

tests = [
    'cold water tap',
    'water tap running',
    'skid mark road',
    'high visibility vest',
    'safety vest car',
    'first aid cross',
    'first aid box',
    'cervical collar',
    'burn dressing',
    'eye bandage',
    'splint leg'
]

for t in tests:
    res = search(t)
    print(f"{t:22} -> {res[:3]}")
    time.sleep(1.0)
