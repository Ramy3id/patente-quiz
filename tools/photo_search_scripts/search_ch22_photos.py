import os
import sys
import time
import json
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

TARGET_DIR = 'assets/images/first_aid_parts'
os.makedirs(TARGET_DIR, exist_ok=True)

USER_AGENT = 'PatenteDidattica/1.0 (https://patente-quiz.it; info@patente-quiz.it) Python-urllib'

def search_commons(query, limit=5):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrsearch={urllib.parse.quote(query)}&gsrlimit={limit}&prop=imageinfo&iiprop=url|size|mime"
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            results = []
            for k, v in pages.items():
                title = v.get('title', '')
                ii = v.get('imageinfo', [{}])[0]
                img_url = ii.get('url', '')
                mime = ii.get('mime', '')
                size = ii.get('size', 0)
                if 'jpg' in mime or 'jpeg' in mime or 'png' in mime:
                    results.append({'title': title, 'url': img_url, 'size': size})
            return results
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return []

queries = {
    'tasso_alcolemico': 'blood alcohol test breathalyzer',
    'tempo_reazione': 'driver braking reaction car stop',
    'visione_tunnel': 'tunnel vision night driving',
    'etilometro_polizia': 'police breathalyzer etilometro alcotest',
    'sostanze_stupefacenti': 'drug test screening saliva urine',
    'farmaci_sonnolenza': 'medicine pills sedative blister pack',
    'chiamata_emergenza_112': 'emergency ambulance 112 paramedic',
    'sicurezza_soccorritore': 'warning triangle reflective safety vest car accident',
    'posizione_laterale_sicurezza': 'recovery position first aid',
    'emorragia_tamponamento': 'first aid bandage wound pressure gauze',
    'stato_di_shock': 'emergency thermal space blanket shock first aid',
    'fratture_immobilizzazione': 'first aid splint limb fracture',
    'infortunato_ustioni': 'first aid burns cold water treatment',
    'corpo_estraneo_occhio': 'eye bandage first aid medical gauze',
    'casco_motociclista': 'motorcycle helmet first aid neck spine',
    'divieti_soccorritore': 'first aid medical cross prohibited pills alcol',
    'gallery_etilometro': 'Dräger Alcotest breathalyzer police',
    'gallery_kit_soccorso': 'car first aid kit DIN 13164',
    'gallery_coperta_termica': 'space blanket thermal survival emergency',
    'gallery_casco_sicurezza': 'motorcycle helmet accident protection',
    'gallery_drug_test': 'rapid drug screen test cassette',
    'gallery_gilet_triangolo': 'warning triangle reflective vest emergency kit'
}

print(f"Starting Wikimedia search for {len(queries)} topics...")
for key, q in queries.items():
    print(f"\n--- Searching: {key} ({q}) ---")
    res = search_commons(q, limit=3)
    for r in res:
        print(f"  Found: {r['title']} | Size: {r['size']} bytes | URL: {r['url']}")
    time.sleep(1.5)
