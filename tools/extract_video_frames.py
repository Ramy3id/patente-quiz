import sys
sys.stdout.reconfigure(encoding='utf-8')
import cv2
import os

video_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793711501662_37023bc9.mp4'
out_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total frames: {total_frames}, FPS: {fps}")

# Extract 5 evenly spaced frames
indices = [0, total_frames // 4, total_frames // 2, 3 * total_frames // 4, total_frames - 1]
for i, frame_idx in enumerate(indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if ret:
        out_path = os.path.join(out_dir, f'video_frame_{i}.png')
        cv2.imwrite(out_path, frame)
        print(f"Saved video_frame_{i}.png at frame {frame_idx}")

cap.release()
