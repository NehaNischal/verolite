import cv2
import numpy as np
import os

video_path = r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4"
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

os.makedirs(r"c:\Users\user\Desktop\verolite\scratch\render_test", exist_ok=True)

# Let's define the composition parameters:
# Target Canvas: 1920 x 1080
CANVAS_W = 1920
CANVAS_H = 1080

# We want the chandelier ring in the final shot to be centered vertically around Y=450-500
# and horizontally on the right half (around X=1350)
# Original video is 720w x 900h.
# If we scale it slightly to fit height or comfortable size:
# Scale factor: 1080 / 900 = 1.2 -> 864w x 1080h.
# If y_offset = 60, the ring (at y=220 in 900h -> 264 in 1080h) will be at Y = 60 + 264 = 324px.
# If y_offset = 120, ring will be at Y = 120 + 264 = 384px.
# Let's test y_offset = 120, x_offset = 1920 - 864 - 50 = 1006.

SCALE = 1.15 # 828w x 1035h
scaled_w = int(720 * SCALE)
scaled_h = int(900 * SCALE)
x_offset = CANVAS_W - scaled_w - 60 # ~ 1032
y_offset = 80 # ring at ~ 80 + 230*1.15 = 345

def process_frame(frame, frame_idx):
    # 1. Clean the text area (y: 570 to 800 in 720x900)
    # Background around text is dark gradient from y=550 to 850
    # In frames where text appears (frame_idx > 150), we replace the text region with smooth vertical background interpolation
    f = frame.copy()
    if frame_idx > 140:
        # Sample top background row at y=560 and bottom row at y=820
        top_row = f[560:565, :].mean(axis=0, keepdims=True) # 1 x 720 x 3
        bot_row = f[820:825, :].mean(axis=0, keepdims=True) # 1 x 720 x 3
        # Interpolate between y=565 and y=820 (height = 255)
        num_rows = 820 - 565
        interp = np.zeros((num_rows, 720, 3), dtype=np.float32)
        for r in range(num_rows):
            weight = r / float(num_rows)
            interp[r] = (1.0 - weight) * top_row + weight * bot_row
        f[565:820, :] = np.clip(interp, 0, 255).astype(np.uint8)

    # 2. Feather all 4 edges of the frame to blend seamlessly into black
    # left/right feather: 80px, top feather: 60px, bottom feather: 60px
    fade_x = 80
    fade_y = 60
    
    alpha_x = np.ones(f.shape[1], dtype=np.float32)
    alpha_x[:fade_x] = np.linspace(0, 1, fade_x)**1.5
    alpha_x[-fade_x:] = np.linspace(1, 0, fade_x)**1.5
    
    alpha_y = np.ones(f.shape[0], dtype=np.float32)
    alpha_y[:fade_y] = np.linspace(0, 1, fade_y)**1.5
    alpha_y[-fade_y:] = np.linspace(1, 0, fade_y)**1.5
    
    alpha_2d = np.outer(alpha_y, alpha_x)[:, :, np.newaxis]
    f_blended = (f.astype(np.float32) * alpha_2d).astype(np.uint8)

    # 3. Resize
    f_scaled = cv2.resize(f_blended, (scaled_w, scaled_h), interpolation=cv2.INTER_LANCZOS4)

    # 4. Composite onto 1920x1080 canvas
    canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)
    
    # Calculate placement bounds
    y1 = max(0, y_offset)
    y2 = min(CANVAS_H, y_offset + scaled_h)
    x1 = max(0, x_offset)
    x2 = min(CANVAS_W, x_offset + scaled_w)
    
    fy1 = max(0, -y_offset)
    fy2 = fy1 + (y2 - y1)
    fx1 = max(0, -x_offset)
    fx2 = fx1 + (x2 - x1)
    
    canvas[y1:y2, x1:x2] = f_scaled[fy1:fy2, fx1:fx2]
    return canvas

# Test on key frames
for sec in [1, 3, 5, 7, 8, 9]:
    idx = min(int(sec * fps), total - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if ret:
        out_canvas = process_frame(frame, idx)
        cv2.imwrite(rf"c:\Users\user\Desktop\verolite\scratch\render_test\comp_sec_{sec}.jpg", out_canvas)
        print(f"Rendered sec {sec}")

cap.release()
