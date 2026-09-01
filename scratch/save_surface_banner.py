import cv2
import shutil

src_path = r"C:\Users\user\.gemini\antigravity-ide\brain\f60bb9cd-7ee0-42e4-83c6-aed06201c81d\.user_uploaded\media_1788298404087.png"
img = cv2.imread(src_path)
h, w, _ = img.shape
print(f"Uploaded surface lights image size: {w}x{h}")

# Save full image as images/surface-hero-banner.jpg
cv2.imwrite(r"images\surface-hero-banner.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
print("Saved images/surface-hero-banner.jpg")

# Also create square crop centered on the white and black fixtures for carousel cards
# The fixtures are centered horizontally and vertically
side = min(h, w)
# Center crop
start_x = (w - side) // 2
start_y = 0 # keep top ceiling anchor
square_crop = img[0:side, start_x:start_x+side]
cv2.imwrite(r"images\collection-2.jpg", square_crop, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
print("Saved images/collection-2.jpg square crop")
