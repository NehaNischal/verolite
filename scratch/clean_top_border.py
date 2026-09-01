import cv2
import numpy as np

img = cv2.imread(r"images\collection-10.jpg")

# The clean top border strip from x=430 to 630, y=110 to 140
clean_strip = img[112:138, 430:630].copy()

# Place it at x=180 to 380, y=112 to 138
# Feather slightly at ends for seamless transition
img[112:138, 182:382] = clean_strip

# And the top background above y=112 for x in [170, 380]:
# In the original, the studio background at y in [50, 112] is smooth gray.
# Let's smooth any residual in x in [25, 180], y in [40, 112] by horizontal interpolation
for y in range(40, 112):
    bg_left = img[y, 10:25].mean(axis=0)
    bg_right = img[y, 660:700].mean(axis=0)
    for x in range(25, 400):
        w_r = (x - 25) / 375.0
        img[y, x] = (1.0 - w_r) * bg_left + w_r * bg_right

# Save to all dimmer image paths
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, img)

print("Applied clean top edge strip!")
