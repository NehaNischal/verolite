import glob, cv2, os

mp4_files = glob.glob(r"c:\Users\user\Desktop\verolite\*.mp4")
for mp in mp4_files:
    cap = cv2.VideoCapture(mp)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    size = os.path.getsize(mp) / (1024*1024)
    print(f"{os.path.basename(mp)}: {w}x{h}, {fps} fps, {total} frames, {size:.2f} MB")
    cap.release()
