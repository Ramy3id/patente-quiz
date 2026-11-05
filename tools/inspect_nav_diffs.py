from PIL import Image

def inspect_diffs():
    names = ["capitoli_index", "capitolo_01", "parole_quiz", "piano_studio", "scheda_esame"]
    # crop navbar of each (120 to 1320, 10 to 80)
    for n in names:
        im = Image.open(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\nav_page_{n}.png")
        nav_crop = im.crop((130, 10, 1310, 80))
        nav_crop.save(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_{n}.png")
    print("Cropped navs saved")

inspect_diffs()
