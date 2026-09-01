import cv2
import numpy as np

orig = cv2.imread(r"scratch\original_arco-7.jpg")
h, w, _ = orig.shape

x_left = 250
x_center = 705
half_width = x_center - x_left # 455

right_part = orig[:, x_center : x_center + half_width]
flipped_right = cv2.flip(right_part, 1)

# Mask for the top gold band region on the left:
# y in [80, 420], x in [x_left, x_center]
mask = np.zeros((h, w), dtype=np.float32)
for y in range(80, 420):
    for x in range(x_left, x_center):
        fx = min((x - x_left) / 20.0, (x_center - x) / 20.0, 1.0)
        fy = min((y - 80) / 20.0, (420 - y) / 20.0, 1.0)
        mask[y, x] = max(0.0, fx * fy)

result = orig.copy()
for c in range(3):
    sub_orig = result[:, x_left:x_center, c]
    sub_flip = flipped_right[:, :, c]
    sub_mask = mask[:, x_left:x_center]
    result[:, x_left:x_center, c] = (1.0 - sub_mask) * sub_orig + sub_mask * sub_flip

# Any dark text pixels outside the cylinder in the top-left background (x < 330, y < 180):
# Simply inpaint or sample clean background at x=200
for y in range(80, 190):
    for x in range(180, 330):
        # If dark pixel from the 'C' or 'O':
        if orig[y, x].mean() < 160:
            result[y, x] = orig[y, 150]

cv2.imwrite(r"images\surface\arco-7.jpg", result)
print("Saved perfect arco-7.jpg!")
