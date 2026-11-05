import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
for name in ['icon-192.png', 'icon-512.png', 'apple-touch-icon.png']:
    p = rf'R:\Ramy\PATENTE_PRO_APP\assets\icons\{name}'
    try:
        im = Image.open(p)
        print(f"{name}: size={im.size}, mode={im.mode}, format={im.format}")
    except Exception as e:
        print(f"Error {name}: {e}")
