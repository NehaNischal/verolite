import cv2
import shutil

src = r"C:\Users\user\.gemini\antigravity-ide\brain\f60bb9cd-7ee0-42e4-83c6-aed06201c81d\.user_uploaded\media_1788296957571.png"
img = cv2.imread(src)

if img is not None:
    # Save as high-quality JPG and PNG
    cv2.imwrite(r"images\strip\nexo-ip65.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    cv2.imwrite(r"images\strip\nexo-ip65.png", img)
    print("Saved images/strip/nexo-ip65.jpg and .png from user-uploaded reel image!")
else:
    print("Failed to load src image")
