import cv2
import numpy as np

def restore_arco_with_symmetry(fname):
    orig = cv2.imread(rf"scratch\original_{fname}")
    h, w, _ = orig.shape
    
    # Cylinder vertical axis of symmetry is x ≈ 700 (w/2)
    # The clean right half is x in [700, 1150]
    # The text region is x in [250, 700], y in [80, 400]
    
    # 1. Flip the right half horizontally:
    flipped_right = cv2.flip(orig[:, 700:], 1) # width is 700, x=0 in flipped is x=700 in orig
    
    # 2. Only blend in the top gold/rim region where the text was:
    # Text was in y in [80, 250], x in [260, 680]
    # Let's create a soft mask for the text quadrant (x in [260, 680], y in [80, 320])
    mask = np.zeros((h, w), dtype=np.float32)
    
    # Soft box mask with feathered edges
    for y in range(80, 320):
        for x in range(260, 680):
            # Smooth fade at boundaries
            fade_x = min((x - 260) / 30.0, (680 - x) / 30.0, 1.0)
            fade_y = min((y - 80) / 30.0, (320 - y) / 30.0, 1.0)
            mask[y, x] = max(0.0, fade_x * fade_y)
            
    # Apply symmetry to left half:
    result = orig.copy()
    left_symmetry = flipped_right[:, :700]
    
    for c in range(3):
        result[:, :700, c] = (1.0 - mask[:, :700]) * orig[:, :700, c] + mask[:, :700] * left_symmetry[:, :, c]
        
    # In addition, ensure background outside the cylinder (x in [100, 400], y in [50, 180]) matches studio gray:
    # Studio background is uniform gray RGB (217, 217, 219)
    bg_color = orig[100, 100]
    for y in range(50, 140):
        for x in range(100, 350):
            if np.linalg.norm(result[y, x].astype(int) - bg_color.astype(int)) > 15:
                # Outside cylinder
                if y < 140 and x < 300:
                    result[y, x] = bg_color
                    
    cv2.imwrite(rf"images\surface\{fname}", result)
    print(f"Restored {fname} with perfect physical symmetry!")

restore_arco_with_symmetry("arco-7.jpg")
restore_arco_with_symmetry("arco-8.jpg")
