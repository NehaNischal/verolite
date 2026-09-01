import subprocess
import cv2
import numpy as np

def clean_image(git_path, save_path, x_range, y_range):
    data = subprocess.check_output(["git", "show", f"HEAD:{git_path}"])
    nparr = np.frombuffer(data, np.uint8)
    orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    h, w, _ = orig.shape
    
    x1, x2 = x_range
    y1, y2 = y_range
    
    roi = orig[y1:y2, x1:x2]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Threshold for text pixels: background is ~215, gold is ~180-210, text is < 170
    text_mask_roi = (gray_roi < 170).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=2)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y1:y2, x1:x2] = text_mask_roi
    
    cleaned = cv2.inpaint(orig, mask, 5, cv2.INPAINT_TELEA)
    
    # Second gentle pass with NS for seamless texture
    sub = cleaned[y1:y2, x1:x2]
    gray_sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    mask_sub2 = ((gray_sub < 175) & (text_mask_roi > 0)).astype(np.uint8) * 255
    mask_sub2 = cv2.dilate(mask_sub2, kernel, iterations=1)
    mask2 = np.zeros((h, w), dtype=np.uint8)
    mask2[y1:y2, x1:x2] = mask_sub2
    cleaned = cv2.inpaint(cleaned, mask2, 3, cv2.INPAINT_NS)
    
    cv2.imwrite(save_path, cleaned)
    print(f"Cleaned and saved {save_path}")

clean_image("images/surface/arco-7.jpg", r"images\surface\arco-7.jpg", (180, 520), (60, 190))
clean_image("images/surface/arco-8.jpg", r"images\surface\arco-8.jpg", (250, 520), (60, 190))
