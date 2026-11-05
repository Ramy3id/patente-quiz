from PIL import Image

def make_hover_comparison():
    img_before = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\card_hover_current.png")
    img_after = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\luxury_card_hover_light.png")
    
    w, h = img_before.size
    canvas = Image.new("RGB", (w * 2 + 40, h + 60), (248, 250, 252))
    
    canvas.paste(img_before, (10, 40))
    canvas.paste(img_after, (w + 30, 40))
    canvas.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\hover_before_after.png")
    print("Saved hover_before_after.png")

make_hover_comparison()
