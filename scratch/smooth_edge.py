import cv2
import numpy as np

img = cv2.imread(r"images\collection-10.jpg")

# Smooth the top glass edge strip y in [108, 128], x in [210, 360]
strip = img[108:128, 210:360]
smoothed_strip = cv2.medianBlur(strip, 5)
img[108:128, 210:360] = cv2.addWeighted(strip, 0.3, smoothed_strip, 0.7, 0)

# Also at top-left corner x in [200, 230], y in [105, 120]
corner_strip = img[105:122, 205:240]
img[105:122, 205:240] = cv2.medianBlur(corner_strip, 5)

# Save to all copies
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, img)

print("Saved smooth dimmer images!")
