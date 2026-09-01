import subprocess
import cv2
import numpy as np

# Load original pristine image
data = subprocess.check_output(["git", "show", "HEAD:images/collection-10.jpg"])
nparr = np.frombuffer(data, np.uint8)
orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

h, w, _ = orig.shape

# Let's create a precise mask of ONLY the dark text letters
# Text 1: "LED Phace" (y: 60-140, x: 30-320)
# Text 2: "Cut Dimmer" (y: 140-200, x: 30-360)
roi = orig[50:210, 20:380]
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# The text pixels are dark (< 155)
# In white glass area (where bg > 230), text is < 190.
# In gray bg area (where bg ~ 205), text is < 160.
text_mask_roi = np.zeros(gray_roi.shape, dtype=np.uint8)

# Glass region inside ROI (approx x > 155 and y > 95)
for r in range(gray_roi.shape[0]):
    for c in range(gray_roi.shape[1]):
        val = gray_roi[r, c]
        # Text detection:
        if val < 165:
            text_mask_roi[r, c] = 255

# Apply 3x3 dilation
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=2)

full_mask = np.zeros((h, w), dtype=np.uint8)
full_mask[50:210, 20:380] = text_mask_roi

# Inpaint using Fast Marching Method (Telea) with small radius=4
cleaned = cv2.inpaint(orig, full_mask, 4, cv2.INPAINT_TELEA)

# Clean bottom watermark if any
mask_bot = np.zeros((h, w), dtype=np.uint8)
gray_bot = cv2.cvtColor(orig[720:, :], cv2.COLOR_BGR2GRAY)
mask_bot[720:, :] = ((gray_bot < 210) & (gray_bot > 160)).astype(np.uint8) * 255
mask_bot = cv2.dilate(mask_bot, kernel, iterations=2)
cleaned = cv2.inpaint(cleaned, mask_bot, 4, cv2.INPAINT_TELEA)

paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, cleaned)

print("Saved cleanly inpaint-restored dimmer images!")
