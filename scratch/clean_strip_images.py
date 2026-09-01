import cv2
import numpy as np
import shutil

# 1. Clean NEXO-COB (remove 'REO' text at bottom-left y in [1000, 1400], x in [100, 600])
cob = cv2.imread(r"images\strip\nexo-cob.jpg")
h, w, _ = cob.shape
roi = cob[1000:, :600]
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
text_mask_roi = (gray_roi < 100).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=3)

mask = np.zeros((h, w), dtype=np.uint8)
mask[1000:, :600] = text_mask_roi

cleaned_cob = cv2.inpaint(cob, mask, 5, cv2.INPAINT_TELEA)
cv2.imwrite(r"images\strip\nexo-cob.jpg", cleaned_cob)
print("Cleaned NEXO-COB (removed REO text)")

# 2. Clean NEXO: copy the clean outdoor-hero-banner without text
shutil.copy2(r"images\outdoor-hero-banner.jpg", r"images\strip\nexo.jpg")
print("Cleaned NEXO (replaced with clean outdoor neon banner)")
