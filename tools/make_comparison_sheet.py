from PIL import Image, ImageDraw, ImageFont

def make_comparison_sheet():
    top_l = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_top_light.png")
    bot_l = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_bottom_light.png")
    
    top_d = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_top_dark.png")
    bot_d = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\compare_bottom_dark.png")
    
    w, h = top_l.size
    
    # Combined Light Mode Canvas
    # Header: 60px, Top Nav: h, Gap: 40px, Bot Nav: h, Padding: 40px
    canvas_w = w + 80
    canvas_h = 60 + h + 60 + h + 60
    
    # Light canvas
    c_l = Image.new("RGB", (canvas_w, canvas_h), (248, 250, 252))
    draw_l = ImageDraw.Draw(c_l)
    
    # Paste top
    c_l.paste(top_l, (40, 70))
    # Paste bottom
    c_l.paste(bot_l, (40, 70 + h + 60))
    c_l.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\stacked_comparison_light.png")
    
    # Dark canvas
    c_d = Image.new("RGB", (canvas_w, canvas_h), (9, 9, 11))
    c_d.paste(top_d, (40, 70))
    c_d.paste(bot_d, (40, 70 + h + 60))
    c_d.save(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\stacked_comparison_dark.png")
    print("Comparison sheets created!")

make_comparison_sheet()
