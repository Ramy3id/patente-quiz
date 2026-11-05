import cv2
import os

video_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793890113497_2360da5e.mp4'
cap = cv2.VideoCapture(video_path)

out_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\hover_sequence'
os.makedirs(out_dir, exist_ok=True)

frame_idx = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if 50 <= frame_idx <= 120:
        # crop cards row 2 (capitolo 06, 05, 04)
        crop = frame[400:750, 50:1250]
        cv2.imwrite(os.path.join(out_dir, f"f_{frame_idx:03d}.png"), crop)
    frame_idx += 1

cap.release()
print("Saved hover sequence frames!")
