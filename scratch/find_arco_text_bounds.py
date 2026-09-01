import cv2, numpy as np

for fname in ["arco-7.jpg", "arco-8.jpg"]:
    orig = cv2.imread(rf"scratch\original_{fname}")
    h, w, _ = orig.shape
    
    # Text is in the top-left quadrant: y in [50, 400], x in [150, 800]
    sub = orig[50:400, 150:800]
    gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    
    # Text pixels are dark gray (< 100)
    dark_y, dark_x = np.where(gray < 100)
    if len(dark_x) > 0:
        min_x, max_x = dark_x.min() + 150, dark_x.max() + 150
        min_y, max_y = dark_y.min() + 50, dark_y.max() + 50
        print(f"{fname} text bounds: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}]")
