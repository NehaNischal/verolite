import subprocess
import cv2
import numpy as np

# Extract untouched original from git
data = subprocess.check_output(["git", "show", "HEAD:images/collection-10.jpg"])
nparr = np.frombuffer(data, np.uint8)
orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

h, w, _ = orig.shape

# The text "LED Phace Cut Dimmer" is in roi: y in [30, 200], x in [20, 360]
roi = orig[30:200, 20:360]
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# Find dark text pixels
# Note: background on left is ~205, glass face is ~245
# Text is < 155
text_mask_roi = (gray_roi < 155).astype(np.uint8) * 255

# Apply minimal 1px dilation so we don't bleed across edges
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=1)

mask = np.zeros((h, w), dtype=np.uint8)
mask[30:200, 20:360] = text_mask_roi

# Inpaint with radius 2
cleaned = cv2.inpaint(orig, mask, 2, cv2.INPAINT_TELEA)

# Second pass on any tiny remaining dark letter pixels with radius 1
sub_clean = cleaned[30:200, 20:360]
gray_sub = cv2.cvtColor(sub_clean, cv2.COLOR_BGR2GRAY)
mask_sub2 = ((gray_sub < 165) & (text_mask_roi > 0)).astype(np.uint8) * 255
mask2 = np.zeros((h, w), dtype=np.uint8)
mask2[30:200, 20:360] = mask_sub2
cleaned = cv2.inpaint(cleaned, mask2, 1, cv2.INPAINT_NS)

# Save to all dimmer image paths
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, cleaned)

print("Saved precise 1px glyph inpainting!")
