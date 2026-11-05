from PIL import Image, ImageChops

im60 = Image.open(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_motion_crops\frame_060.png')
im75 = Image.open(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_motion_crops\frame_075.png')

diff = ImageChops.difference(im60, im75)
bbox = diff.getbbox()
print("Motion bounding box 60->75:", bbox)

im140 = Image.open(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_motion_crops\frame_140.png')
im180 = Image.open(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_motion_crops\frame_180.png')
diff2 = ImageChops.difference(im140, im180)
print("Motion bounding box 140->180:", diff2.getbbox())

# Let's crop the bbox area
if bbox:
    crop1 = im75.crop(bbox)
    crop1.save(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\user_action_area.png')
