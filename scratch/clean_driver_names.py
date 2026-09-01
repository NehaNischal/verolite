import cv2
import numpy as np

def clean_driver_image(path):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not load {path}")
        return
    
    h, w, _ = img.shape
    # The text is located at the bottom portion (y in [750, 1000])
    roi_y1 = int(h * 0.75)
    
    roi = img[roi_y1:, :]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Text pixels are distinctly darker (< 130) than the light grey background (> 180)
    text_mask_roi = (gray_roi < 130).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=3)
    
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[roi_y1:, :] = text_mask_roi
    
    cleaned = cv2.inpaint(img, full_mask, 7, cv2.INPAINT_TELEA)
    
    cv2.imwrite(path, cleaned, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"Cleaned {path} successfully!")

driver_files = [
    r"images\drivers\driver-ip65.jpg",
    r"images\drivers\constant-voltage-dimming-ip65.jpg",
    r"images\drivers\constant-voltage-dimming-ip20.jpg",
    r"images\drivers\constant-current-dimming.jpg"
]

for df in driver_files:
    clean_driver_image(df)
