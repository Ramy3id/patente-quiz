import cv2

video_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793890113497_2360da5e.mp4'
cap = cv2.VideoCapture(video_path)

# Print frame indices where mouse is hovering
# Let's save frames every 10 frames from 0 to 240
step = 10
idx = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if idx % 15 == 0:
        cv2.imwrite(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_frames\vframe_{idx:03d}.png", frame)
    idx += 1

cap.release()
print("Saved vframes")
