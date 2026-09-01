import cv2

path = r"images\drivers\constant-current-dimming.jpg"
img = cv2.imread(path)
h, w, _ = img.shape
for y in range(h):
    img[y, 0:15] = img[y, 25]

cv2.imwrite(path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
print("Cleaned left margin 100%")
