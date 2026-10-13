import os
import sys
import time
import json
import urllib.request
import urllib.parse
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

TARGET_DIR = 'assets/images/first_aid_parts'
os.makedirs(TARGET_DIR, exist_ok=True)

USER_AGENT = 'PatenteDidattica/1.0 (https://patente-quiz.it; info@patente-quiz.it) Python-urllib'

# Map of target file names to Wikimedia Commons titles
PHOTO_MAP = {
    # 16 Cards
    'tasso_alcolemico.jpg': 'File:Simulation of Motorist Blood-Alcohol Level Test - NARA - 6925433.jpg',
    'tempo_reazione.jpg': 'File:Lane with skid marks - geograph.org.uk - 554950.jpg',
    'visione_tunnel.jpg': 'File:Old Komine Tunnel at Night 2026.jpg',
    'etilometro_polizia.jpg': 'File:Cop, police station, breathalyzer, test (1980s) - NARA - 8452397.jpg',
    'sostanze_stupefacenti.jpg': 'File:Urine drug screen.jpg',
    'farmaci_sonnolenza.jpg': 'File:Pills in blister pack.jpg',
    'chiamata_emergenza_112.jpg': 'File:Ambulanza Croce Rossa Italiana Bolzano CRI+565 AH.jpg',
    'sicurezza_soccorritore.jpg': 'File:Warnweste gelb.jpg',
    'posizione_laterale_sicurezza.jpg': 'File:Coma Position.jpg',
    'emorragia_tamponamento.jpg': 'File:Gauze 03.JPG',
    'stato_di_shock.jpg': 'File:RescueFoil.jpg',
    'fratture_immobilizzazione.jpg': 'File:Leg splint.jpg',
    'infortunato_ustioni.jpg': 'File:Running water tap.jpg',
    'corpo_estraneo_occhio.jpg': 'File:Nurse with small child with eye bandage (4644488125).jpg',
    'casco_motociclista.jpg': 'File:Cervical collar.jpg',
    'divieti_soccorritore.jpg': 'File:Red Cross first aid station - Malvern Spring Show 2010.jpg',
    
    # 6 Workshop Gallery
    'gallery_etilometro.jpg': 'File:Dräger Alcotest 3000 (1).JPG',
    'gallery_kit_soccorso.jpg': 'File:Car first aid Kits.png',
    'gallery_coperta_termica.jpg': 'File:Emergency blanket 20110709.jpg',
    'gallery_casco_sicurezza.jpg': 'File:Full-Face Helmet 9274.jpg',
    'gallery_drug_test.jpg': 'File:Urine drug screen.jpg',
    'gallery_gilet_triangolo.jpg': 'File:Red triangle of a car.jpg'
}

def resolve_commons_url(title):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for k, v in pages.items():
                ii = v.get('imageinfo', [])
                if ii:
                    return ii[0].get('url')
    except Exception as e:
        print(f"Error resolving {title}: {e}")
    return None

def download_and_optimize(target_filename, title):
    out_path = os.path.join(TARGET_DIR, target_filename)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"[EXISTS] {target_filename} already downloaded and optimized.")
        return True
    
    img_url = resolve_commons_url(title)
    if not img_url:
        print(f"[FAIL] Could not get URL for {title}")
        return False
    
    tmp_path = out_path + '.tmp'
    req = urllib.request.Request(img_url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            with open(tmp_path, 'wb') as f:
                f.write(resp.read())
        
        # Optimize with PIL
        with Image.open(tmp_path) as im:
            im = im.convert('RGB')
            # target size max width 900
            max_size = (900, 600)
            im.thumbnail(max_size, Image.Resampling.LANCZOS)
            im.save(out_path, 'JPEG', quality=85, optimize=True)
        
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
        print(f"[OK] Downloaded and optimized {target_filename} ({os.path.getsize(out_path)} bytes)")
        return True
    except Exception as e:
        print(f"[ERROR] Failed {target_filename}: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False

print(f"Downloading and optimizing {len(PHOTO_MAP)} images...")
success = 0
for target, title in PHOTO_MAP.items():
    ok = download_and_optimize(target, title)
    if ok:
        success += 1
    time.sleep(1.2)

print(f"\nDone! Successfully processed {success}/{len(PHOTO_MAP)} images.")
