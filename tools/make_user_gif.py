from PIL import Image
import os

folder = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\hover_sequence'
files = sorted([f for f in os.listdir(folder) if f.startswith('f_') and f.endswith('.png')])

imgs = [Image.open(os.path.join(folder, f)) for f in files[::2]] # every 2nd frame
gif_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\user_experience.gif'
imgs[0].save(gif_path, save_all=True, append_images=imgs[1:], duration=66, loop=0)
print("Saved user_experience.gif")
