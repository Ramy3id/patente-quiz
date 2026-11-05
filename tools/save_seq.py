import cv2

video_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793890113497_2360da5e.mp4'
cap = cv2.VideoCapture(video_path)

# Find what the user was doing
# Let's save frames 60 to 120 every 2 frames
frame_idx = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if 60 <= frame_idx <= 120 and frame_idx % 2 == 0:
        cv2.imwrite(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_frames\seq_{frame_idx:03d}.png", frame[380:760, 20:850])
    frame_idx += 1

cap.release()
print("Saved seq frames")
