import os
import sys
import time
import json
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = 'PatenteDidattica/1.0 (https://patente-quiz.it; info@patente-quiz.it) Python-urllib'

def search_commons(query, limit=4):
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
        return []

simple_queries = {
    'tasso_alcolemico': 'breathalyzer test',
    'tempo_reazione': 'car braking skid',
    'visione_tunnel': 'tunnel night road',
    'etilometro_polizia': 'police breathalyzer',
    'sostanze_stupefacenti': 'drug test cassette',
    'farmaci_sonnolenza': 'blister pack pills',
    'chiamata_emergenza_112': 'emergency ambulance',
    'sicurezza_soccorritore': 'warning triangle car',
    'posizione_laterale_sicurezza': 'recovery position',
    'emorragia_tamponamento': 'gauze bandage',
    'stato_di_shock': 'space blanket emergency',
    'fratture_immobilizzazione': 'first aid splint',
    'infortunato_ustioni': 'burn treatment cold water',
    'corpo_estraneo_occhio': 'eye bandage',
    'casco_motociclista': 'motorcycle helmet',
    'divieti_soccorritore': 'first aid no medicine',
    'gallery_etilometro': 'Dräger Alcotest',
    'gallery_kit_soccorso': 'car first aid kit',
    'gallery_coperta_termica': 'space blanket foil',
    'gallery_casco_sicurezza': 'motorcycle helmet white',
    'gallery_drug_test': 'drug screen test',
    'gallery_gilet_triangolo': 'reflective vest car'
}

found = {}
for k, q in simple_queries.items():
    res = search_commons(q, limit=3)
    found[k] = res
    print(f"Key: {k:28} | Results: {len(res)} -> {[r['title'][:40] for r in res]}")
    time.sleep(1.2)

with open('found_ch22_urls.json', 'w', encoding='utf-8') as f:
    json.dump(found, f, ensure_ascii=False, indent=2)
