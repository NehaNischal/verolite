import cv2
import numpy as np

def perfect_arco(fname):
    orig = cv2.imread(rf"scratch\original_{fname}")
    h, w, _ = orig.shape
    
    # Measure cylinder bounds at mid-height (y = 600)
    row = orig[600, :, :]
    bg_color = orig[50, 50]
    
    # Find cylinder width where color diverges from background
    diff = np.linalg.norm(row.astype(float) - bg_color.astype(float), axis=1)
    cyl_x = np.where(diff > 25)[0]
    x_left = int(cyl_x.min())
    x_right = int(cyl_x.max())
    x_center = int(round((x_left + x_right) / 2.0))
    half_width = x_center - x_left
    print(f"{fname}: x_left={x_left}, x_right={x_right}, x_center={x_center}, half_width={half_width}")
    
    # The right half of the cylinder is from x_center to x_center + half_width
    right_part = orig[:, x_center : x_center + half_width]
    flipped_right = cv2.flip(right_part, 1) # width = half_width
    
    # In the original image, only the text region needs replacement:
    # Text region: y in [90, 420], x in [x_left, x_center]
    mask = np.zeros((h, w), dtype=np.float32)
    for y in range(80, 450):
        for x in range(x_left, x_center):
            fx = min((x - x_left) / 20.0, (x_center - x) / 20.0, 1.0)
            fy = min((y - 80) / 20.0, (450 - y) / 20.0, 1.0)
            mask[y, x] = max(0.0, fx * fy)
            
    result = orig.copy()
    
    # Replace left side
    for c in range(3):
        sub_orig = result[:, x_left:x_center, c]
        sub_flip = flipped_right[:, :, c]
        sub_mask = mask[:, x_left:x_center]
        result[:, x_left:x_center, c] = (1.0 - sub_mask) * sub_orig + sub_mask * sub_flip
        
    # Clean any residual above top rim:
    # Find top rim Y as a function of X from the right half:
    rim_y = {}
    for rx in range(x_center, x_center + half_width):
        col = orig[:500, rx]
        col_diff = np.linalg.norm(col.astype(float) - bg_color.astype(float), axis=1)
        top_pts = np.where(col_diff > 20)[0]
        if len(top_pts) > 0:
            rim_y[rx - x_center] = top_pts.min()
            
    # Apply clean background above rim for all X:
    for dx, y_top in rim_y.items():
        lx = x_center - dx
        rx = x_center + dx
        for y in range(0, y_top - 1):
            if 0 <= lx < w:
                result[y, lx] = bg_color
            if 0 <= rx < w:
                result[y, rx] = bg_color
                
    # Also background to left of x_left and above y=500
    for x in range(0, x_left):
        for y in range(0, 500):
            result[y, x] = bg_color

    cv2.imwrite(rf"images\surface\{fname}", result)
    print(f"Perfected {fname}")

perfect_arco("arco-7.jpg")
perfect_arco("arco-8.jpg")
