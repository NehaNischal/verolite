import cv2
import numpy as np

def clean_arco_7():
    img = cv2.imread(r"images\surface\arco-7.jpg")
    h, w, _ = img.shape
    
    # Text 'CO-7' is at top-left: y in [60, 180], x in [180, 500]
    roi = img[60:180, 180:500]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Dark text pixels (< 100)
    text_mask_roi = (gray_roi < 110).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=2)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[60:180, 180:500] = text_mask_roi
    
    # Inpaint
    cleaned = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    # Second fine pass
    sub = cleaned[60:180, 180:500]
    gray_sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    mask_sub2 = ((gray_sub < 130) & (text_mask_roi > 0)).astype(np.uint8) * 255
    mask2 = np.zeros((h, w), dtype=np.uint8)
    mask2[60:180, 180:500] = mask_sub2
    cleaned = cv2.inpaint(cleaned, mask2, 2, cv2.INPAINT_NS)
    
    cv2.imwrite(r"images\surface\arco-7.jpg", cleaned)
    print("Cleaned arco-7.jpg")

def clean_arco_8():
    img = cv2.imread(r"images\surface\arco-8.jpg")
    h, w, _ = img.shape
    
    # Text 'CO-8' / 'O-8' is at top-left: y in [60, 180], x in [250, 500]
    roi = img[60:180, 250:500]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Dark text pixels (< 110)
    text_mask_roi = (gray_roi < 110).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=2)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[60:180, 250:500] = text_mask_roi
    
    # Inpaint
    cleaned = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    # Second fine pass
    sub = cleaned[60:180, 250:500]
    gray_sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    mask_sub2 = ((gray_sub < 130) & (text_mask_roi > 0)).astype(np.uint8) * 255
    mask2 = np.zeros((h, w), dtype=np.uint8)
    mask2[60:180, 250:500] = mask_sub2
    cleaned = cv2.inpaint(cleaned, mask2, 2, cv2.INPAINT_NS)
    
    cv2.imwrite(r"images\surface\arco-8.jpg", cleaned)
    print("Cleaned arco-8.jpg")

clean_arco_7()
clean_arco_8()
