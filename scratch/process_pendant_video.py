import cv2
import numpy as np

src_video = r"Pendant_light_product_video_202609020317.mp4"
out_video = r"pendant-light-hero-video.mp4"

cap = cv2.VideoCapture(src_video)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Processing {total_frames} frames ({w}x{h} @ {fps}fps)...")

fourcc = cv2.VideoWriter_fourcc(*'avc1')
out = cv2.VideoWriter(out_video, fourcc, fps, (w, h))

# Inpaint watermark mask in bottom right: y in [550, 640], x in [1120, 1200]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# Also capture the best frame (illuminated ring light) for hero poster hero.jpg
# Frame 180 is the peak illuminated hero frame
cap.set(cv2.CAP_PROP_POS_FRAMES, 180)
ret, hero_frame = cap.read()
if ret:
    # Inpaint watermark on hero_frame
    roi = hero_frame[550:645, 1115:1205]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    mask_roi = (gray_roi > 90).astype(np.uint8) * 255
    mask_roi = cv2.dilate(mask_roi, kernel, iterations=2)
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[550:645, 1115:1205] = mask_roi
    cleaned_hero = cv2.inpaint(hero_frame, full_mask, 5, cv2.INPAINT_TELEA)
    cv2.imwrite("hero.jpg", cleaned_hero, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print("Saved illuminated hero.jpg poster frame!")

# Rewind to start
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

frame_num = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # Inpaint watermark
    roi = frame[550:645, 1115:1205]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    mask_roi = (gray_roi > 85).astype(np.uint8) * 255
    if np.sum(mask_roi) > 0:
        mask_roi = cv2.dilate(mask_roi, kernel, iterations=2)
        full_mask = np.zeros((h, w), dtype=np.uint8)
        full_mask[550:645, 1115:1205] = mask_roi
        frame = cv2.inpaint(frame, full_mask, 5, cv2.INPAINT_TELEA)
        
    out.write(frame)
    frame_num += 1
    if frame_num % 60 == 0:
        print(f"Processed frame {frame_num}/{total_frames}")

cap.release()
out.release()
print("Exported pendant-light-hero-video.mp4 successfully!")
