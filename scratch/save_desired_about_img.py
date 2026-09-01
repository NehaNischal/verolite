import cv2
import shutil

src = r"C:\Users\user\.gemini\antigravity-ide\brain\f60bb9cd-7ee0-42e4-83c6-aed06201c81d\.user_uploaded\media_1788301290183.png"
img = cv2.imread(src)

if img is not None:
    cv2.imwrite(r"images\about-img.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    cv2.imwrite(r"images\about-story.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print("Saved user's desired image to images/about-img.jpg and images/about-story.jpg successfully!")
else:
    print("Error reading image")
