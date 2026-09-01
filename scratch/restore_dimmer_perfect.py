import cv2
import numpy as np

# Load fresh original from scratch_outdoor_zip or backup if exists, or repair collection-10
# Let's inspect where the glass top edge is:
img = cv2.imread(r"images\collection-10.jpg")
h, w, _ = img.shape

# In the right half of the image (x > 400), the top edge of the glass bevel is:
# Let's find horizontal gradient / edge
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# The top glass border highlight on the right is around y=135-155.
# Let's clone the clean region from x=450 to x=650 (width 200) to cover x=180 to x=380 and x=280 to x=480.
clean_glass_top = img[120:200, 430:650].copy() # 80 high x 220 wide

# The top-left corner of the glass plate:
# Left edge of the glass plate is at x ≈ 178.
# Top edge of the glass plate is at y ≈ 138.
# The white frosted glass plate body starts below y=148.

# Let's replace the top edge strip x in [178, 430], y in [120, 200] with the clean glass top:
img[120:200, 210:430] = clean_glass_top

# For x in [178, 210], we mirror the left edge:
# The corner top-left is at (178, 138).
# Clean background above the plate (y < 135) across the whole top:
for y in range(0, 135):
    # smooth background from right side
    bg_color = img[y, 700:780].mean(axis=0)
    img[y, :650] = bg_color

# Clean left background (x < 178, y in 0 to 700):
for x in range(0, 178):
    for y in range(0, 700):
        img[y, x] = img[y, 740] # match smooth right background

# Clean bottom watermark artifacts:
for y in range(710, h):
    img[y, :] = img[705, :]

# Save to all copies
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, img)

print("Restored clean dimmer image perfectly!")
