import cv2
import os

video_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793890113497_2360da5e.mp4'
cap = cv2.VideoCapture(video_path)

out_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_motion_crops'
os.makedirs(out_dir, exist_ok=True)

frame_idx = 0
targets = [60, 65, 70, 75, 80, 85, 140, 150, 160, 170, 180]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_idx in targets:
        cv2.imwrite(os.path.join(out_dir, f"frame_{frame_idx:03d}.png"), frame)
    frame_idx += 1

cap.release()
print("Saved target frames")
