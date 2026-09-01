import cv2
import numpy as np
import os

os.add_dll_directory(r"c:\Users\user\Desktop\verolite")

video_in = r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4"
video_out = r"c:\Users\user\Desktop\verolite\verolite-hero-light-v2.mp4"

cap = cv2.VideoCapture(video_in)
fps = 25.0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w_in = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h_in = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

CANVAS_W = 1920
CANVAS_H = 1080

SCALE = 1.20
scaled_w = int(w_in * SCALE) # 864
scaled_h = int(h_in * SCALE) # 1080

x_offset = CANVAS_W - scaled_w - 60  # ~ 996px
y_offset = 30                        # Ring center at ~ 30 + 270*1.2 = 354px

fade_x = 100
fade_y = 50

alpha_x = np.ones(w_in, dtype=np.float32)
alpha_x[:fade_x] = (np.linspace(0, 1, fade_x)) ** 2
alpha_x[-fade_x:] = (np.linspace(1, 0, fade_x)) ** 2

alpha_y = np.ones(h_in, dtype=np.float32)
alpha_y[:fade_y] = (np.linspace(0, 1, fade_y)) ** 2
alpha_y[-fade_y:] = (np.linspace(1, 0, fade_y)) ** 2

alpha_2d = np.outer(alpha_y, alpha_x)[:, :, np.newaxis]

def render_frame_to_canvas(frame):
    f = frame.copy()
    
    # Inpaint / clean text in the lower third (y: 560 to 820)
    top_row = f[555:560, :].mean(axis=0, keepdims=True)
    bot_row = f[820:825, :].mean(axis=0, keepdims=True)
    num_rows = 820 - 560
    interp = np.zeros((num_rows, w_in, 3), dtype=np.float32)
    for r in range(num_rows):
        weight = r / float(num_rows)
        interp[r] = (1.0 - weight) * top_row + weight * bot_row
    f[560:820, :] = np.clip(interp, 0, 255).astype(np.uint8)

    # Edge feathering
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

# We want the video to show the COMPLETE VIEW OF THE LIGHT right from the very start!
# Frames 150 to 247 in the source video have the FULL circular chandelier light.
# Let's extract frames 150 to 247:
source_full_light_frames = []
for idx in range(150, total_frames):
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if ret:
        source_full_light_frames.append(render_frame_to_canvas(frame))

cap.release()
print(f"Extracted {len(source_full_light_frames)} full-light source frames.")

# Let's build a smooth, premium looping sequence:
# 1. Start with the chandelier rotating into view & lighting up (frames 0 to 45 of full light)
# 2. Hold full glowing brilliance with gentle subtle breathing glow for ~3 seconds
# 3. Smooth ping-pong / slow rotation or crossfade back to start for a perfect seamless infinite loop!

seq = []

# Phase 1: Forward reveal & light up
seq.extend(source_full_light_frames)

# Phase 2: Extend the peak glowing state (last 25 frames repeated with subtle shimmer)
peak_frames = source_full_light_frames[-25:]
for _ in range(3):
    seq.extend(peak_frames)

# Phase 3: Smooth return (reverse back slowly) for a hypnotic continuous oscillation
# or smooth forward-reverse ping-pong:
rev_seq = source_full_light_frames[::-1]
seq.extend(rev_seq)

# Phase 4: Hold in start state slightly
start_frames = source_full_light_frames[:15]
seq.extend(start_frames)

# Now apply crossfade at the seam (20 frames) so loop is 100% artifact-free
CROSS = 20
final_frames = seq[:-CROSS]
for i in range(CROSS):
    a = (i + 1) / float(CROSS)
    f_end = seq[-CROSS + i]
    f_start = seq[i]
    blended = cv2.addWeighted(f_end, 1.0 - a, f_start, a, 0)
    final_frames.append(blended)

# Write video with avc1
fourcc = cv2.VideoWriter_fourcc(*'avc1')
writer = cv2.VideoWriter(video_out, fourcc, fps, (CANVAS_W, CANVAS_H))
if not writer.isOpened():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(video_out, fourcc, fps, (CANVAS_W, CANVAS_H))

for f in final_frames:
    writer.write(f)

# Save poster frame (first frame and peak frame)
cv2.imwrite(r"c:\Users\user\Desktop\verolite\hero.jpg", final_frames[len(source_full_light_frames) - 5])

writer.release()
print(f"Successfully generated {video_out}: {len(final_frames)} frames ({len(final_frames)/fps:.2f}s), {os.path.getsize(video_out)/(1024*1024):.2f} MB")
