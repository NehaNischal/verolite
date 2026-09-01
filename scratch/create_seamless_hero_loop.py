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

CANVAS_W = 1920
CANVAS_H = 1080

# We want the chandelier ring in the final shot to be clearly visible, prominent, and elegant.
# Original frame: 720w x 900h
# Ring in original is at y=180 to 360 (center at y=270).
# Let's scale slightly: SCALE = 1.15 -> 828w x 1035h.
# If we set y_offset = 120:
# Ring center will be at Y = 120 + 270*1.15 = 430px (right in the sweet spot of the 1080p hero viewport!).
# X offset = 1920 - 828 - 60 = 1032px (centered in the right half of the 1920px screen).

SCALE = 1.15
scaled_w = int(w_in * SCALE)
scaled_h = int(h_in * SCALE)
x_offset = CANVAS_W - scaled_w - 60
y_offset = 120

fade_x = 100
fade_y = 60

alpha_x = np.ones(w_in, dtype=np.float32)
alpha_x[:fade_x] = (np.linspace(0, 1, fade_x)) ** 2
alpha_x[-fade_x:] = (np.linspace(1, 0, fade_x)) ** 2

alpha_y = np.ones(h_in, dtype=np.float32)
alpha_y[:fade_y] = (np.linspace(0, 1, fade_y)) ** 2
alpha_y[-fade_y:] = (np.linspace(1, 0, fade_y)) ** 2

alpha_2d = np.outer(alpha_y, alpha_x)[:, :, np.newaxis]

def render_canvas(frame, frame_idx):
    f = frame.copy()
    
    # Inpaint / clean text in the lower third
    if frame_idx > 130:
        top_row = f[560:565, :].mean(axis=0, keepdims=True)
        bot_row = f[820:825, :].mean(axis=0, keepdims=True)
        num_rows = 820 - 565
        interp = np.zeros((num_rows, w_in, 3), dtype=np.float32)
        for r in range(num_rows):
            weight = r / float(num_rows)
            interp[r] = (1.0 - weight) * top_row + weight * bot_row
        f[565:820, :] = np.clip(interp, 0, 255).astype(np.uint8)

    f_blended = (f.astype(np.float32) * alpha_2d).astype(np.uint8)
    f_scaled = cv2.resize(f_blended, (scaled_w, scaled_h), interpolation=cv2.INTER_LANCZOS4)

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
    return canvas

# Read all frames into list
all_canvases = []
for idx in range(total_frames):
    ret, frame = cap.read()
    if not ret:
        break
    all_canvases.append(render_canvas(frame, idx))
cap.release()

print(f"Rendered {len(all_canvases)} source frames.")

# Let's extend the final glowing state (frame 220 to 247)
# by adding ~2.5 seconds (60 frames) of the glowing chandelier
# so the audience has ample time to appreciate the full fixture!
last_glow_frames = all_canvases[220:245]
extended_frames = list(all_canvases)
# Repeat a subtle gentle pulse / hold
for _ in range(2):
    extended_frames.extend(last_glow_frames)

# Now let's create a smooth 1-second (25 frames) crossfade loop from the end back to the start!
CROSSFADE = 25
total_ext = len(extended_frames)
final_video_frames = extended_frames[:total_ext - CROSSFADE]

for i in range(CROSSFADE):
    alpha = (i + 1) / float(CROSSFADE)
    # Blend end of extended with beginning of video
    frame_from_end = extended_frames[total_ext - CROSSFADE + i]
    frame_from_start = extended_frames[i]
    blended = cv2.addWeighted(frame_from_end, 1.0 - alpha, frame_from_start, alpha, 0)
    final_video_frames.append(blended)

# Write to video
fourcc = cv2.VideoWriter_fourcc(*'avc1')
writer = cv2.VideoWriter(video_out, fourcc, fps, (CANVAS_W, CANVAS_H))
if not writer.isOpened():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(video_out, fourcc, fps, (CANVAS_W, CANVAS_H))

for f in final_video_frames:
    writer.write(f)

# Update poster frame
cv2.imwrite(r"c:\Users\user\Desktop\verolite\hero.jpg", all_canvases[230])

writer.release()
print(f"Done! Final video has {len(final_video_frames)} frames ({len(final_video_frames)/fps:.2f}s). File size: {os.path.getsize(video_out)/(1024*1024):.2f} MB")
