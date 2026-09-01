import subprocess
import cv2
import numpy as np

# Load original pristine image
data = subprocess.check_output(["git", "show", "HEAD:images/collection-10.jpg"])
nparr = np.frombuffer(data, np.uint8)
orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

h, w, _ = orig.shape

# The text "LED Phace Cut Dimmer" is ONLY in:
# y: 40 to 180, x: 25 to 350
# Let's create a precise mask only for the dark letter pixels:
text_roi = orig[40:180, 25:350]
gray_roi = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)

# Dark text threshold
text_mask = (gray_roi < 160).astype(np.uint8) * 255

# Dilate by 2px
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
text_mask = cv2.dilate(text_mask, kernel, iterations=2)

full_mask = np.zeros((h, w), dtype=np.uint8)
full_mask[40:180, 25:350] = text_mask

# Inpaint using Telea with radius 3
cleaned = cv2.inpaint(orig, full_mask, 3, cv2.INPAINT_TELEA)

# Second very gentle pass on any residual letter shadows
sub = cleaned[40:180, 25:350]
gray_sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
text_mask2 = ((gray_sub < 168) & (text_mask > 0)).astype(np.uint8) * 255
full_mask2 = np.zeros((h, w), dtype=np.uint8)
full_mask2[40:180, 25:350] = text_mask2
cleaned = cv2.inpaint(cleaned, full_mask2, 2, cv2.INPAINT_NS)

# Save to all copies
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, cleaned)

print("Saved clean dimmer image without touching any other part of the image!")
