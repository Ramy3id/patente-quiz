import cv2

video_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793890113497_2360da5e.mp4'
cap = cv2.VideoCapture(video_path)

# Sample every 1 second (every 30 frames)
for i in range(0, 250, 30):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(rf"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\video_frames\time_{i//30}s.png", frame)

cap.release()
print("Saved time frames 0s to 8s")
