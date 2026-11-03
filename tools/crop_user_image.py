from PIL import Image

img = Image.open(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793704830910_f96e0a8a.png')
w, h = img.size
print("Image size:", w, h)
# Save cropped buttons
cropped = img.crop((0, int(h * 0.3), w, h))
cropped.save(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\cropped_user_buttons.png')
print("Cropped image saved successfully!")
