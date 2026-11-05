from PIL import Image, ImageChops

im1 = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_capitoli_index.png")
im2 = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_capitolo_01.png")

diff = ImageChops.difference(im1, im2)
print("Crop diff bbox:", diff.getbbox())

# Let's inspect where pixels differ
if diff.getbbox():
    # Find bounding boxes of differing areas
    diff.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_diff.png")
    print("Saved crop_diff.png")
