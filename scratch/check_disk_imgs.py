import cv2

img9 = cv2.imread(r"images\collection-9.jpg")
img10 = cv2.imread(r"images\collection-10.jpg")

cv2.imwrite(r"scratch\check_disk_9.jpg", img9)
cv2.imwrite(r"scratch\check_disk_10.jpg", img10)
print("Saved disk check images")
