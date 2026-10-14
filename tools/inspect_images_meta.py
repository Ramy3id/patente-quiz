import os, glob, sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

folders = [
    'assets/images/autostrada_parts',
    'assets/images/lighting_parts',
    'assets/images/safety_parts',
    'assets/images/patente_parts',
    'assets/images/weather_parts',
    'assets/images/first_aid_parts',
    'assets/images/insurance_parts',
    'assets/images/eco_parts',
    'assets/images/vehicle_parts'
]

for folder in folders:
    if not os.path.exists(folder):
        print(f"Folder missing: {folder}")
        continue
    files = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.png', '.webp'))]
    print(f"=== {folder} ({len(files)} images) ===")
    for f in files[:4]:
        p = os.path.join(folder, f)
        sz = os.path.getsize(p)
        try:
            with Image.open(p) as img:
                w, h = img.size
                fmt = img.format
                print(f"   {f}: {fmt} {w}x{h}, {sz//1024} KB")
        except Exception as e:
            print(f"   {f}: error reading image: {e}")
