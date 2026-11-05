import sys
import os
import json
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

repo = r'R:\Ramy\PATENTE_PRO_APP'
app_icon_src = os.path.join(repo, 'assets', 'brand', 'app_store_icon_proposal7.png')
icons_dir = os.path.join(repo, 'assets', 'icons')

im = Image.open(app_icon_src).convert('RGBA')

# 1. Generate icon-192.png
im_192 = im.resize((192, 192), Image.Resampling.LANCZOS)
im_192.save(os.path.join(icons_dir, 'icon-192.png'), format='PNG', optimize=True)

# 2. Generate icon-512.png
im_512 = im.resize((512, 512), Image.Resampling.LANCZOS)
im_512.save(os.path.join(icons_dir, 'icon-512.png'), format='PNG', optimize=True)

# 3. Generate icon-maskable-512.png (with safe zone padding for Android adaptive icons)
# Android maskable icons need 10-15% padding so circular/squircle masking doesn't cut edges
maskable = Image.new('RGBA', (512, 512), (11, 15, 25, 255)) # Dark navy background
# Resize icon to 410x410 (80% safe zone) and paste in center
im_safe = im.resize((410, 410), Image.Resampling.LANCZOS)
maskable.paste(im_safe, (51, 51), im_safe)
maskable.save(os.path.join(icons_dir, 'icon-maskable-512.png'), format='PNG', optimize=True)

# 4. Generate apple-touch-icon.png (180x180)
im_apple = im.resize((180, 180), Image.Resampling.LANCZOS)
im_apple.save(os.path.join(icons_dir, 'apple-touch-icon.png'), format='PNG', optimize=True)
im_apple.save(os.path.join(repo, 'apple-touch-icon.png'), format='PNG', optimize=True)

print("SUCCESS: Generated 192, 512, maskable-512, and apple-touch-icon!")

# 5. Overwrite icon.svg so it NEVER renders the traffic light again!
# Create an SVG that embeds the base64 or links cleanly
import base64
with open(os.path.join(icons_dir, 'icon-512.png'), 'rb') as f:
    b64_data = base64.b64encode(f.read()).decode('utf-8')

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <image width="512" height="512" href="data:image/png;base64,{b64_data}"/>
</svg>'''

with open(os.path.join(icons_dir, 'icon.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_content)
print("SUCCESS: Replaced icon.svg with new official brand icon!")

# 6. Update manifest.json with cache-busting version query
manifest_path = os.path.join(repo, 'manifest.json')
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

manifest['icons'] = [
    {
        "src": "./assets/icons/icon-192.png?v=20261104_v4",
        "sizes": "192x192",
        "type": "image/png",
        "purpose": "any"
    },
    {
        "src": "./assets/icons/icon-512.png?v=20261104_v4",
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "any"
    },
    {
        "src": "./assets/icons/icon-maskable-512.png?v=20261104_v4",
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "maskable"
    }
]

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("SUCCESS: Updated manifest.json with dedicated maskable and any icons!")

# 7. Update service-worker.js cache name
sw_path = os.path.join(repo, 'service-worker.js')
with open(sw_path, 'r', encoding='utf-8') as f:
    sw_code = f.read()

import re
sw_code = re.sub(r"const CACHE_NAME = ['\"][^'\"]+['\"];", "const CACHE_NAME = 'patente-pro-v2026-11-04-V4-OFFICIAL';", sw_code)

with open(sw_path, 'w', encoding='utf-8') as f:
    f.write(sw_code)

print("SUCCESS: Bumped CACHE_NAME in service-worker.js to v2026-11-04-V4-OFFICIAL")
