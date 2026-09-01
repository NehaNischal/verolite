import cv2
import numpy as np
import os

# 1. Clean collection-9.jpg (and driver-ip20.jpg copies)
def clean_driver_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return
    h, w, _ = img.shape
    
    # Text "Led Strip Light Driver IP20" is in bottom left
    # Let's create a mask for inpainting or sample surrounding studio background
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Text region: y > h * 0.70, x < w * 0.65
    y_start = int(h * 0.70)
    x_end = int(w * 0.65)
    
    # Find text pixels (they are darker than the light gray background)
    sub = img[y_start:, :x_end]
    gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    
    # Background in this region is around gray value 190-205.
    # Text is dark gray/black (< 150)
    text_mask_sub = (gray < 160).astype(np.uint8) * 255
    
    # Dilate mask slightly for clean edges
    kernel = np.ones((5, 5), np.uint8)
    text_mask_sub = cv2.dilate(text_mask_sub, kernel, iterations=2)
    
    mask[y_start:, :x_end] = text_mask_sub
    
    # Inpaint with radius 7
    cleaned = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)
    
    # Also smooth any subtle residual in the text bounding box with the smooth background gradient
    bg_sample = img[y_start:, int(w*0.75):].mean(axis=1, keepdims=True) # smooth vertical profile
    # Let's ensure perfectly smooth clean background
    cleaned = cv2.inpaint(cleaned, mask, 5, cv2.INPAINT_NS)
    
    cv2.imwrite(img_path, cleaned)
    print(f"Cleaned {img_path}")

# 2. Clean collection-10.jpg (and phase-cut-dimmer.jpg copies)
def clean_dimmer_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return
    h, w, _ = img.shape
    
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Top left text region: y < h * 0.28, x < w * 0.50
    y_end = int(h * 0.28)
    x_end = int(w * 0.50)
    sub = img[:y_end, :x_end]
    gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    
    # Text is dark (< 150), background is ~195-210
    text_mask_sub = (gray < 155).astype(np.uint8) * 255
    kernel = np.ones((5, 5), np.uint8)
    text_mask_sub = cv2.dilate(text_mask_sub, kernel, iterations=2)
    mask[:y_end, :x_end] = text_mask_sub
    
    # Bottom watermark residue: y > h * 0.94
    y_bot = int(h * 0.94)
    sub_bot = img[y_bot:, :]
    gray_bot = cv2.cvtColor(sub_bot, cv2.COLOR_BGR2GRAY)
    bot_mask = (np.abs(gray_bot.astype(int) - int(gray_bot.mean())) > 3).astype(np.uint8) * 255
    bot_mask = cv2.dilate(bot_mask, kernel, iterations=2)
    mask[y_bot:, :] = bot_mask
    
    cleaned = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
    cleaned = cv2.inpaint(cleaned, mask, 3, cv2.INPAINT_NS)
    
    cv2.imwrite(img_path, cleaned)
    print(f"Cleaned {img_path}")

# Target paths
driver_paths = [
    r"images\collection-9.jpg",
    r"images\drivers\driver-ip20.jpg",
    r"images\outdoor\driver-ip20.jpg"
]

dimmer_paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in driver_paths:
    if os.path.exists(p):
        clean_driver_image(p)

for p in dimmer_paths:
    if os.path.exists(p):
        clean_dimmer_image(p)

print("All target images processed!")
