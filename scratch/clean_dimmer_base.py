import cv2
import numpy as np

banner = cv2.imread(r"images\dimmer\dimmer-hero-banner.jpg")
bh, bw, _ = banner.shape

# Fill the bottom blend area under dimmer with smooth background
bot_col = np.array([195, 194, 196], dtype=np.uint8)
# The dimmer bottom edge is at y ≈ 770
# Let's fix y in [765, 850], x in [700, 1300]
for y in range(770, bh):
    alpha = (y - 770) / (bh - 770)
    for x in range(650, 1350):
        banner[y, x] = banner[y, 500]

cv2.imwrite(r"images\dimmer\dimmer-hero-banner.jpg", banner, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
print("Cleaned bottom base of dimmer-hero-banner.jpg")
