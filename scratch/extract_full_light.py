import cv2
import os

cap = cv2.VideoCapture(r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

os.makedirs(r"c:\Users\user\Desktop\verolite\scratch\full_light_frames", exist_ok=True)

# Let's save frames from 140 to 247 in steps of 5
for f in range(140, total, 5):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(rf"c:\Users\user\Desktop\verolite\scratch\full_light_frames\f_{f}.jpg", frame)

cap.release()
print("Saved full light frames from 140 to", total)
