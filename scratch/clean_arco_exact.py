import cv2
import numpy as np

def clean_arco(fname, x_bounds, y_bounds):
    orig = cv2.imread(rf"scratch\original_{fname}")
    h, w, _ = orig.shape
    
    x1, x2 = x_bounds
    y1, y2 = y_bounds
    
    # Expand by 20px padding
    px1 = max(0, x1 - 20)
    px2 = min(w, x2 + 20)
    py1 = max(0, y1 - 20)
    py2 = min(h, y2 + 20)
    
    roi = orig[py1:py2, px1:px2]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Background and gold are > 160, text is < 120
    text_mask_roi = (gray_roi < 135).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=3)
    
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[py1:py2, px1:px2] = text_mask_roi
    
    # Inpaint with Telea radius 5
    cleaned = cv2.inpaint(orig, full_mask, 5, cv2.INPAINT_TELEA)
    
    # Fine pass with NS
    sub = cleaned[py1:py2, px1:px2]
    gray_sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    mask_sub2 = ((gray_sub < 145) & (text_mask_roi > 0)).astype(np.uint8) * 255
    mask_sub2 = cv2.dilate(mask_sub2, kernel, iterations=1)
    mask2 = np.zeros((h, w), dtype=np.uint8)
    mask2[py1:py2, px1:px2] = mask_sub2
    cleaned = cv2.inpaint(cleaned, mask2, 3, cv2.INPAINT_NS)
    
    cv2.imwrite(rf"images\surface\{fname}", cleaned)
    print(f"Cleaned images\\surface\\{fname}")

clean_arco("arco-7.jpg", (270, 680), (110, 240))
clean_arco("arco-8.jpg", (340, 810), (110, 410))
