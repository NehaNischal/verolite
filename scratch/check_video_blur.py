import cv2

cap = cv2.VideoCapture(r"Pendant_light_product_video_202609020317.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Save frames every 10 frames from 0 to 120
for f in range(0, 120, 10):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"scratch/frame_{f:03d}.jpg", frame)

cap.release()
print("Saved frames 0 to 110")
