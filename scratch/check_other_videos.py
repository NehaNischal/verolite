import cv2

for fname in ["hero page video.mp4", "hero page video (original with text).mp4", "hero-video.mp4"]:
    try:
        cap = cv2.VideoCapture(fname)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        dur = total / fps if fps > 0 else 0
        print(f"{fname}: {w}x{h}, {fps} fps, {total} frames, {dur:.2f}s")
        cap.release()
    except Exception as e:
        print(f"Error {fname}: {e}")
