import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

p = r'R:\Ramy\PATENTE_PRO_APP\manifest.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Manifest name:', data.get('name'))
print('Manifest short_name:', data.get('short_name'))
print('Icons:')
for ico in data.get('icons', []):
    src = ico.get('src')
    full_path = os.path.normpath(os.path.join(r'R:\Ramy\PATENTE_PRO_APP', src))
    exists = os.path.exists(full_path)
    size = os.path.getsize(full_path) if exists else 0
    print(f"  - src: {src} | sizes: {ico.get('sizes')} | purpose: {ico.get('purpose')} | exists: {exists} | size: {size} bytes")
