from PIL import Image

thumbs = []
for s in range(8):
    im = Image.open(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_frames\time_{s}s.png")
    # crop cards area
    crop = im.crop((50, 150, 1250, 750))
    crop = crop.resize((400, 200))
    thumbs.append(crop)

sheet = Image.new("RGB", (820, 840), (255, 255, 255))
for i, t in enumerate(thumbs):
    col = i % 2
    row = i // 2
    sheet.paste(t, (10 + col * 410, 10 + row * 210))

sheet.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_timeline.png")
print("Saved video_timeline.png")
