import subprocess
import cv2
import numpy as np

# Extract binary data directly from git
data = subprocess.check_output(["git", "show", "HEAD:images/collection-10.jpg"])
nparr = np.frombuffer(data, np.uint8)
orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

h, w, _ = orig.shape
print(f"Loaded original collection-10: {w}x{h}")

# The text "LED Phace Cut Dimmer" is located at:
# x: 30 to 350, y: 50 to 190
roi = orig[50:190, 25:350]
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# The letters are dark text on light background (< 160)
letter_mask_roi = (gray_roi < 160).astype(np.uint8) * 255

# Apply small dilation (3x3 ellipse)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
letter_mask_roi = cv2.dilate(letter_mask_roi, kernel, iterations=2)

mask = np.zeros((h, w), dtype=np.uint8)
mask[50:190, 25:350] = letter_mask_roi

# Inpaint with Navier-Stokes method, inpaintRadius=3
result = cv2.inpaint(orig, mask, 3, cv2.INPAINT_NS)

# Clean any tiny remaining speckles
mask2 = np.zeros((h, w), dtype=np.uint8)
sub2 = result[50:190, 25:350]
gray2 = cv2.cvtColor(sub2, cv2.COLOR_BGR2GRAY)
mask2[50:190, 25:350] = ((gray2 < 165) & (letter_mask_roi > 0)).astype(np.uint8) * 255
result = cv2.inpaint(result, mask2, 3, cv2.INPAINT_TELEA)

cv2.imwrite(r"images\collection-10.jpg", result)
cv2.imwrite(r"images\dimmer\phase-cut-dimmer.jpg", result)
cv2.imwrite(r"images\outdoor\phase-cut-dimmer.jpg", result)
cv2.imwrite(r"images\outdoor\phase-cut-dimmer-2.jpg", result)

print("Saved pristine cleaned dimmer images!")
