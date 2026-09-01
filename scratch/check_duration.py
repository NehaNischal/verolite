import cv2

cap = cv2.VideoCapture(r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("Total frames in original:", total, "FPS:", fps)

# Check frame 170, 180, 190, 200, 210, 220, 230, 240, 247
for f in range(160, total, 10):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if ret:
        print(f"Frame {f} (time {f/fps:.2f}s): mean brightness = {frame.mean():.2f}")

cap.release()
