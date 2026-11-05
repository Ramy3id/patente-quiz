from PIL import Image
import os

out_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_frames'
files = sorted([f for f in os.listdir(out_dir) if f.endswith('.png')])

for f in files[:8]:
    im = Image.open(os.path.join(out_dir, f))
    # crop card 1 area
    # In 1302x910, cards are roughly in the middle
    crop = im.crop((100, 200, 1200, 700))
    crop.save(os.path.join(out_dir, f"crop_{f}"))

print("Cropped frames saved!")
