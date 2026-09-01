import cv2
import numpy as np

def clean_sensor(fn, y_frac_start):
    path = f"images/sensors/{fn}"
    img = cv2.imread(path)
    h, w, _ = img.shape
    
    # 1. Clean left margin dark strip if present
    for y in range(h):
        if np.mean(img[y, 0:5]) < 120 and np.mean(img[y, 25:35]) > 165:
            img[y, 0:15] = img[y, 25]
            
    # 2. Text is strictly in y >= int(h * y_frac_start)
    y_start = int(h * y_frac_start)
    roi = img[y_start:, :]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Text is darker (< 160) than background (> 175)
    text_mask_roi = (gray_roi < 162).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=2)
    
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[y_start:, :] = text_mask_roi
    
    cleaned = cv2.inpaint(img, full_mask, 5, cv2.INPAINT_TELEA)
    
    # Clean any faint watermark (< 185) in bottom region
    roi_bot = cleaned[int(h * 0.85):, :]
    gray_bot = cv2.cvtColor(roi_bot, cv2.COLOR_BGR2GRAY)
    bot_mask = ((gray_bot < 184) & (gray_bot > 150)).astype(np.uint8) * 255
    if np.sum(bot_mask) > 0:
        bot_mask = cv2.dilate(bot_mask, kernel, iterations=2)
        mask_bot_full = np.zeros((h, w), dtype=np.uint8)
        mask_bot_full[int(h * 0.85):, :] = bot_mask
        cleaned = cv2.inpaint(cleaned, mask_bot_full, 5, cv2.INPAINT_TELEA)
        
    cv2.imwrite(path, cleaned, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"Cleaned {fn} perfectly!")

# Clean each sensor
clean_sensor("cabinet-door-sensor.jpg", 0.86)
clean_sensor("wireless-motion-sensor.jpg", 0.88)
clean_sensor("wireless-door-sensor.jpg", 0.88)
clean_sensor("partition-touch-handwave-sensor.jpg", 0.84)
