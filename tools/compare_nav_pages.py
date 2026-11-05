from PIL import Image, ImageChops

names = ["capitoli_index", "root_index", "capitolo_01", "parole_quiz", "piano_studio", "scheda_esame"]
base = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\nav_page_capitoli_index.png")

for n in names[1:]:
    im = Image.open(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\nav_page_{n}.png")
    diff = ImageChops.difference(base, im)
    bbox = diff.getbbox()
    print(f"Diff between capitoli_index and {n}: {bbox}")

# Combine them into a contact sheet
canvas = Image.new("RGB", (1440, 150 * len(names)), (255, 255, 255))
for i, n in enumerate(names):
    im = Image.open(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\nav_page_{n}.png")
    canvas.paste(im, (0, i * 150))

canvas.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\all_navs_stacked.png")
print("Saved all_navs_stacked.png")
