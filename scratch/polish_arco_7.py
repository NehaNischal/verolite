import cv2
import numpy as np

# Load original
orig = cv2.imread(r"scratch\original_arco-7.jpg")
h, w, _ = orig.shape

# Current symmetrical result
curr = cv2.imread(r"images\surface\arco-7.jpg")

# The gold cylinder body is in x >= 332 and y in [130, 420]
# The studio background on the left is in x < 332
# Restore the original background for x < 330:
curr[:, :330] = orig[:, :330]

# For the small region of text on the background between x=270 and x=330, y in [115, 180]:
# Background is uniform vertical gradient
for y in range(110, 180):
    for x in range(270, 330):
        # sample clean background from x=240
        curr[y, x] = orig[y, 240]

# Clean tiny center rim notch at (664, 85 to 135)
for y in range(80, 130):
    curr[y, 655:675] = orig[50, 50]

cv2.imwrite(r"images\surface\arco-7.jpg", curr)
print("Saved polished arco-7.jpg!")
