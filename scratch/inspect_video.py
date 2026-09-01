import cv2
import os

video_path = r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4"
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = total_frames / fps if fps > 0 else 0

print(f"Video Info: {width}x{height}, {fps} fps, {total_frames} frames, {duration:.2f} seconds")

# Save several frames across the video to see what happens
os.makedirs(r"c:\Users\user\Desktop\verolite\scratch\frames", exist_ok=True)

frame_indices = [0, int(total_frames*0.25), int(total_frames*0.5), int(total_frames*0.75), int(total_frames*0.9), total_frames - 1]

for idx in frame_indices:
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(rf"c:\Users\user\Desktop\verolite\scratch\frames\frame_{idx}.jpg", frame)
        print(f"Saved frame {idx} (time: {idx/fps:.2f}s)")

cap.release()
