import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

img_path = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793707271569_87d66d82.png"
im = Image.open(img_path)
print("Image size:", im.size)
