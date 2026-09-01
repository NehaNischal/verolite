import cv2
import os

print("Testing VideoWriter with openh264...")
cap = cv2.VideoCapture(r"Pendant_light_product_video_202609020317.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'avc1')
out_path = r"scratch\test_clean_video.mp4"
out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

if not out.isOpened():
    print("avc1 failed, trying H264...")
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

print("VideoWriter isOpened:", out.isOpened())

# Clean watermark on 10 frames as a test
# Watermark mask in bottom right: x in [1120, 1195], y in [560, 635]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
for i in range(10):
    ret, frame = cap.read()
    if not ret:
        break
    roi = frame[550:645, 1110:1205]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    mask_roi = (gray_roi > 100).astype('uint8') * 255
    mask_roi = cv2.dilate(mask_roi, kernel, iterations=2)
    
    full_mask = np.zeros((h, w), dtype='uint8') if 'np' in locals() else None
    
cap.release()
out.release()
print("Success!")
