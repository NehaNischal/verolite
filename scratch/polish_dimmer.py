import cv2
import numpy as np

img = cv2.imread(r"images\collection-10.jpg")
h, w, _ = img.shape

# The glass top edge is at y ≈ 122.
# Let's clean the background above the glass plate:
# For y in range(0, 118) and x < 650:
for y in range(0, 120):
    bg_val = img[y, 700:750].mean(axis=0)
    img[y, :650] = bg_val

# The clean top bevel of the glass plate on the right (x in [420, 620], y in [120, 150])
# has the top glass highlight line and bevel.
top_bevel = img[120:150, 420:620].copy() # 30x200
img[120:150, 200:400] = top_bevel

# For the top-left corner (x in [178, 200], y in [120, 150]):
# Left edge of the glass plate is at x ≈ 178.
corner_bevel = img[120:150, 420:442].copy()
img[120:150, 178:200] = corner_bevel

# Clean the left background outside the glass plate (x < 178, y in [0, 700])
for x in range(0, 178):
    for y in range(0, 700):
        img[y, x] = img[y, 740] # uniform vertical gradient

# Clean bottom watermark residue (y > 720)
for y in range(725, h):
    img[y, :] = img[720, :]

# Save to all dimmer image paths
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, img)

print("Saved perfected dimmer images!")
