from PIL import Image

def crop_sections():
    # Light mode
    img_l = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_nav_light.png")
    w, h = img_l.size
    
    # Crop middle 40% (x from 0.3w to 0.7w, full height)
    mid_l = img_l.crop((int(w * 0.28), 0, int(w * 0.72), h))
    mid_l.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_mid_light.png")
    
    # Dark mode
    img_d = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_nav_dark.png")
    mid_d = img_d.crop((int(w * 0.28), 0, int(w * 0.72), h))
    mid_d.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\pure_white_mid_dark.png")
    print("Cropped middle sections saved!")

crop_sections()
