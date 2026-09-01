import cv2
import numpy as np

def clean_sensor_precise(filename, y_start, y_end):
    path = f"images/sensors/{filename}"
    img = cv2.imread(path)
    h, w, _ = img.shape
    print(f"{filename}: {w}x{h}, cleaning text in y in [{y_start}, {y_end}]")
    
    # 1. Check if there's a dark strip on the left edge (x in [0, 15])
    for y in range(h):
        if np.mean(img[y, 0:5]) < 120 and np.mean(img[y, 25:35]) > 170:
            img[y, 0:15] = img[y, 25]
            
    # 2. Text inpaint strictly in y in [y_start, y_end]
    roi = img[y_start:y_end, :]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Text is darker (< 160) than background (> 180)
    # Exclude any very large contiguous black objects if they exist
    text_mask_roi = (gray_roi < 165).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=2)
    
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[y_start:y_end, :] = text_mask_roi
    
    cleaned = cv2.inpaint(img, full_mask, 5, cv2.INPAINT_TELEA)
    
    # If there's any faint watermark in [y_end, h], also clean it
    roi_bot = cleaned[y_end:, :]
    if roi_bot.shape[0] > 0:
        gray_bot = cv2.cvtColor(roi_bot, cv2.COLOR_BGR2GRAY)
        bot_mask = ((gray_bot < 185) & (gray_bot > 150)).astype(np.uint8) * 255
        if np.sum(bot_mask) > 0:
            bot_mask = cv2.dilate(bot_mask, kernel, iterations=2)
            mask_bot_full = np.zeros((h, w), dtype=np.uint8)
            mask_bot_full[y_end:, :] = bot_mask
            cleaned = cv2.inpaint(cleaned, mask_bot_full, 5, cv2.INPAINT_TELEA)
            
    cv2.imwrite(path, cleaned, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"Cleaned {filename} precisely!")

# 1. cabinet-door-sensor: text is at y=880..960
clean_sensor_precise("cabinet-door-sensor.jpg", 860, 980)

# 2. wireless-motion-sensor: sensor ends at y=815, text is at y=880..960
clean_sensor_precise("wireless-motion-sensor.jpg", 860, 980)

# 3. wireless-door-sensor: sensor ends at y=775, text is at y=880..960
clean_sensor_precise("wireless-door-sensor.jpg", 860, 980)

# 4. partition-touch-handwave-sensor: sensor ends at y=800, text is at y=840..980
clean_sensor_precise("partition-touch-handwave-sensor.jpg", 830, 980)
