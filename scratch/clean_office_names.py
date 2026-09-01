import cv2
import numpy as np

def clean_office_image(path):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not load {path}")
        return
    
    h, w, _ = img.shape
    # The text is located in the bottom-left area: y in [750, 1000], x in [50, 500] (for 1000x1000)
    # The text color is dark grey (< 120), background is light grey (> 180)
    roi_y1 = int(h * 0.70)
    roi_x2 = int(w * 0.55)
    
    roi = img[roi_y1:, :roi_x2]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Text pixels are distinctly darker than the wall background
    text_mask_roi = (gray_roi < 130).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=3)
    
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[roi_y1:, :roi_x2] = text_mask_roi
    
    # Inpaint using Navier-Stokes / Telea
    cleaned = cv2.inpaint(img, full_mask, 7, cv2.INPAINT_TELEA)
    
    cv2.imwrite(path, cleaned, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"Cleaned {path} successfully!")

for img_name in ["lino.jpg", "reo.jpg", "recta.jpg"]:
    clean_office_image(rf"images\office\{img_name}")
