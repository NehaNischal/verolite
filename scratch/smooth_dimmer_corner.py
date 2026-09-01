import cv2

path = r"images\dimmer\phase-cut-dimmer.jpg"
img = cv2.imread(path)
h, w, _ = img.shape

# Clean the bottom-left corner x in [0, 160], y in [680, h]
for y in range(680, h):
    col = img[y, 10]
    img[y, 0:165] = col

cv2.imwrite(path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
cv2.imwrite(r"images\collection-dimmer.jpg", img)
cv2.imwrite(r"images\collection-10.jpg", img)

# Also update banner
import subprocess
subprocess.run(["python", r"c:\Users\user\Desktop\verolite\scratch\clean_dimmer_watermark.py"])
