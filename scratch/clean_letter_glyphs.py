import cv2
import numpy as np

orig = cv2.imread(r"scratch\original_collection_10.jpg")
h, w, _ = orig.shape

# The text "LED Phace Cut Dimmer" is located at:
# x from 30 to 350, y from 60 to 180
# Let's crop this text region and create a precise letter mask
roi = orig[50:190, 20:360]
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# The letters are dark text on light background (background is > 185, letters are < 160)
letter_mask_roi = (gray_roi < 165).astype(np.uint8) * 255

# Apply small morphological opening and dilation (radius 2)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
letter_mask_roi = cv2.dilate(letter_mask_roi, kernel, iterations=1)

# Full mask
mask = np.zeros((h, w), dtype=np.uint8)
mask[50:190, 20:360] = letter_mask_roi

# Inpaint with Navier-Stokes method, inpaintRadius=3
result = cv2.inpaint(orig, mask, 3, cv2.INPAINT_NS)

# Also clean any tiny residue with a second fine pass
mask2 = (cv2.cvtColor(result[50:190, 20:360], cv2.COLOR_BGR2GRAY) < 170).astype(np.uint8) * 255
mask2 = cv2.dilate(mask2, kernel, iterations=1)
mask_pass2 = np.zeros((h, w), dtype=np.uint8)
mask_pass2[50:190, 20:360] = mask2
result = cv2.inpaint(result, mask_pass2, 2, cv2.INPAINT_TELEA)

cv2.imwrite(r"scratch\test_clean_dimmer.jpg", result)
print("Saved test_clean_dimmer.jpg")
