import cv2

video_path = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.user_uploaded\media_1793890113497_2360da5e.mp4'
cap = cv2.VideoCapture(video_path)

# Let's inspect frame by frame around frame 30 to 120
frame_idx = 0
prev_gray = None

diffs = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if prev_gray is not None:
        diff = cv2.absdiff(gray, prev_gray)
        diff_val = diff.sum()
        diffs.append((frame_idx, diff_val))
    prev_gray = gray
    frame_idx += 1

cap.release()
# Sort top diffs
diffs.sort(key=lambda x: x[1], reverse=True)
print("Top moving frames:", diffs[:10])
