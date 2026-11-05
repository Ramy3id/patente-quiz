from PIL import Image

names = [
    ("Capitoli Index (Home)", "universal_capitoli_home.png"),
    ("Capitolo 01", "universal_capitolo_01.png"),
    ("Capitolo 13", "universal_capitolo_13.png"),
    ("Dizionario Sinonimi", "universal_dizionario.png"),
    ("Piano Studio", "universal_piano_studio.png"),
    ("Scheda Esame", "universal_scheda_esame.png")
]

imgs = [Image.open(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\{f}") for _, f in names]
w, h = imgs[0].size

# Create a clean stacked image
stacked = Image.new("RGB", (w + 40, (h + 30) * len(imgs) + 40), (241, 245, 249))

for i, img in enumerate(imgs):
    y = 20 + i * (h + 30)
    stacked.paste(img, (20, y))

stacked.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\unified_navbar_proof.png")
print("Saved unified_navbar_proof.png successfully!")
