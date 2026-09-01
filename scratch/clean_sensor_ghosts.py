import cv2
import numpy as np

def clean_bottom_ghost_watermark(fn):
    path = f"images/sensors/{fn}"
    img = cv2.imread(path)
    h, w, _ = img.shape
    
    # Inpaint any pixel in y >= int(0.86*h) that differs from background
    y_start = int(h * 0.86)
    roi = img[y_start:, :]
    
    # Fill with smooth vertical/horizontal background interpolation
    # Background color is approximately [180, 180, 180] to [195, 195, 195]
    for y in range(y_start, h):
        # sample left and right background colors
        col_l = img[y, 15].astype(np.float32)
        col_r = img[y, w - 15].astype(np.float32)
        for x in range(w):
            alpha = x / (w - 1)
            img[y, x] = ((1 - alpha) * col_l + alpha * col_r).astype(np.uint8)
            
    # Also clean top-left margin if present
    for y in range(h):
        if np.mean(img[y, 0:5]) < 130 and np.mean(img[y, 25:35]) > 165:
            img[y, 0:20] = img[y, 25]
            
    # Also clean top margin for cabinet-door-sensor if dark
    if fn == "cabinet-door-sensor.jpg":
        for x in range(w):
            if np.mean(img[0:10, x]) < 130 and np.mean(img[20:30, x]) > 165:
                img[0:15, x] = img[20, x]

    cv2.imwrite(path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"Cleaned ghost watermark on {fn}")

for fn in ["cabinet-door-sensor.jpg", "wireless-motion-sensor.jpg", "wireless-door-sensor.jpg", "partition-touch-handwave-sensor.jpg"]:
    clean_bottom_ghost_watermark(fn)
