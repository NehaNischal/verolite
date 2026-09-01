import cv2
import numpy as np
import os

os.add_dll_directory(r"c:\Users\user\Desktop\verolite")

video_in = r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4"
video_out = r"c:\Users\user\Desktop\verolite\hero page video.mp4"

cap = cv2.VideoCapture(video_in)
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 25.0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w_in = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h_in = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Input video: {w_in}x{h_in}, {fps} fps, {total_frames} frames")

CANVAS_W = 1920
CANVAS_H = 1080

SCALE = 1.15
scaled_w = int(w_in * SCALE)
scaled_h = int(h_in * SCALE)

x_offset = CANVAS_W - scaled_w - 80  # X center of ring at ~1410
y_offset = 60                       # Y center of ring at ~370

fourcc = cv2.VideoWriter_fourcc(*'avc1')
writer = cv2.VideoWriter(video_out, fourcc, fps, (CANVAS_W, CANVAS_H))

if not writer.isOpened():
    print("Error: Could not open VideoWriter with avc1, trying mp4v")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(video_out, fourcc, fps, (CANVAS_W, CANVAS_H))

print(f"Rendering {total_frames} frames to {video_out}...")

fade_x = 100
fade_y = 60

alpha_x = np.ones(w_in, dtype=np.float32)
alpha_x[:fade_x] = (np.linspace(0, 1, fade_x)) ** 2
alpha_x[-fade_x:] = (np.linspace(1, 0, fade_x)) ** 2

alpha_y = np.ones(h_in, dtype=np.float32)
alpha_y[:fade_y] = (np.linspace(0, 1, fade_y)) ** 2
alpha_y[-fade_y:] = (np.linspace(1, 0, fade_y)) ** 2

alpha_2d = np.outer(alpha_y, alpha_x)[:, :, np.newaxis]

for frame_idx in range(total_frames):
    ret, frame = cap.read()
    if not ret:
        break
    
    f = frame.copy()
    
    # Clean text region (y: 565 to 820)
    if frame_idx > 130:
        top_row = f[560:565, :].mean(axis=0, keepdims=True)
        bot_row = f[820:825, :].mean(axis=0, keepdims=True)
        num_rows = 820 - 565
        interp = np.zeros((num_rows, w_in, 3), dtype=np.float32)
        for r in range(num_rows):
            weight = r / float(num_rows)
            interp[r] = (1.0 - weight) * top_row + weight * bot_row
        f[565:820, :] = np.clip(interp, 0, 255).astype(np.uint8)

    # Edge feathering
    f_blended = (f.astype(np.float32) * alpha_2d).astype(np.uint8)

    # Scale
    f_scaled = cv2.resize(f_blended, (scaled_w, scaled_h), interpolation=cv2.INTER_LANCZOS4)

    # Canvas
    canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)
    
    y1 = max(0, y_offset)
    y2 = min(CANVAS_H, y_offset + scaled_h)
    x1 = max(0, x_offset)
    x2 = min(CANVAS_W, x_offset + scaled_w)
    
    fy1 = max(0, -y_offset)
    fy2 = fy1 + (y2 - y1)
    fx1 = max(0, -x_offset)
    fx2 = fx1 + (x2 - x1)
    
    canvas[y1:y2, x1:x2] = f_scaled[fy1:fy2, fx1:fx2]
    
    writer.write(canvas)
    
    # Save poster frame around frame 220
    if frame_idx == 220:
        cv2.imwrite(r"c:\Users\user\Desktop\verolite\hero.jpg", canvas)

writer.release()
cap.release()

size_mb = os.path.getsize(video_out) / (1024 * 1024)
print(f"Finished successfully! Output size: {size_mb:.2f} MB")
