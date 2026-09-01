import cv2
import os

cap = cv2.VideoCapture(r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

os.makedirs(r"c:\Users\user\Desktop\verolite\scratch\timeline", exist_ok=True)

for sec in range(0, 10):
    frame_idx = min(int(sec * fps), total - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(rf"c:\Users\user\Desktop\verolite\scratch\timeline\sec_{sec}.jpg", frame)
        print(f"Sec {sec} saved")

cap.release()
