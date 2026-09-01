import cv2
import numpy as np

img = cv2.imread(r"images\dimmer\phase-cut-dimmer.jpg")
h, w, c = img.shape
print(f"phase-cut-dimmer.jpg shape: {w}x{h}")

# Background color at corners:
corners = [img[10, 10], img[10, w-10], img[h-10, 10], img[h-10, w-10]]
print("Corner colors BGR:", corners)
avg_bg = np.mean(corners, axis=0)
print("Avg background color BGR:", avg_bg)
