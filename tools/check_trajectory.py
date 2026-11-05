import cv2
import numpy as np

# Find cursor position in frames 60 to 120
# Cursor is white with black outline
cursor_positions = []
for idx in range(60, 121, 2):
    f_path = rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_frames\seq_{idx:03d}.png"
    img = cv2.imread(f_path)
    if img is not None:
        # just print shape
        pass
print("Frames available")
