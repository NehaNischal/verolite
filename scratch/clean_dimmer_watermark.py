import cv2
import numpy as np

# 1. Clean phase-cut-dimmer.jpg: remove faint text in y in [700, 753]
dimmer = cv2.imread(r"images\dimmer\phase-cut-dimmer.jpg")
h, w, _ = dimmer.shape
# Faint text is at the bottom y >= 700
roi = dimmer[680:, :]
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
# text is slightly darker (< 196) than background (~202)
text_mask_roi = ((gray_roi < 198) & (gray_roi > 150)).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
text_mask_roi = cv2.dilate(text_mask_roi, kernel, iterations=2)

mask = np.zeros((h, w), dtype=np.uint8)
mask[680:, :] = text_mask_roi

cleaned_dimmer = cv2.inpaint(dimmer, mask, 5, cv2.INPAINT_TELEA)
cv2.imwrite(r"images\dimmer\phase-cut-dimmer.jpg", cleaned_dimmer)
cv2.imwrite(r"images\collection-dimmer.jpg", cleaned_dimmer)
cv2.imwrite(r"images\collection-10.jpg", cleaned_dimmer)
print("Cleaned faint bottom watermark from phase-cut-dimmer.jpg")

# 2. Re-generate wide banner using the ultra-clean dimmer
dh, dw, _ = cleaned_dimmer.shape
bw, bh = 2000, 850
banner = np.zeros((bh, bw, 3), dtype=np.uint8)

top_col = np.array([193, 192, 194], dtype=np.float32)
bot_col = np.array([203, 202, 204], dtype=np.float32)

for y in range(bh):
    alpha = y / (bh - 1)
    col = (1 - alpha) * top_col + alpha * bot_col
    banner[y, :] = col.astype(np.uint8)

target_dh = 690
target_dw = int(dw * (target_dh / dh))
dimmer_resized = cv2.resize(cleaned_dimmer, (target_dw, target_dh), interpolation=cv2.INTER_LANCZOS4)

start_x = (bw - target_dw) // 2
start_y = (bh - target_dh) // 2

blend_w = 40
alpha_mask = np.ones((target_dh, target_dw), dtype=np.float32)
for i in range(blend_w):
    factor = i / blend_w
    alpha_mask[i, :] *= factor
    alpha_mask[target_dh - 1 - i, :] *= factor
    alpha_mask[:, i] *= factor
    alpha_mask[:, target_dw - 1 - i] *= factor
    
alpha_mask_3d = np.repeat(alpha_mask[:, :, np.newaxis], 3, axis=2)

bg_roi = banner[start_y : start_y + target_dh, start_x : start_x + target_dw].astype(np.float32)
fg_roi = dimmer_resized.astype(np.float32)

blended = (fg_roi * alpha_mask_3d + bg_roi * (1 - alpha_mask_3d)).astype(np.uint8)
banner[start_y : start_y + target_dh, start_x : start_x + target_dw] = blended

# Vignette
y_coords, x_coords = np.ogrid[:bh, :bw]
center_x, center_y = bw // 2, bh // 2
dist = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
max_dist = np.sqrt((bw//2)**2 + (bh//2)**2)
vignette = 1.0 - 0.08 * (dist / max_dist)**1.5
banner_float = banner.astype(np.float32) * vignette[:, :, np.newaxis]
banner = np.clip(banner_float, 0, 255).astype(np.uint8)

cv2.imwrite(r"images\dimmer\dimmer-hero-banner.jpg", banner, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
print("Updated images/dimmer/dimmer-hero-banner.jpg with 100% spotless dimmer!")
