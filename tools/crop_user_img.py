import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

img_path = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793707271569_87d66d82.png"
im = Image.open(img_path)

# Let's crop the VERO / FALSO buttons area: from y=350 to y=500
crop1 = im.crop((0, 360, 444, 460))
crop1.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_vf_user.png")

# Also crop footer area: from y=460 to y=650
crop2 = im.crop((0, 460, 444, 650))
crop2.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_footer_user.png")

print("Cropped successfully!")
