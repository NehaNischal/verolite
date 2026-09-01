import cv2

img_home = cv2.imread(r"C:\Users\user\.gemini\antigravity-ide\brain\f60bb9cd-7ee0-42e4-83c6-aed06201c81d\.user_uploaded\media_1788301290183.png")
img_about = cv2.imread(r"C:\Users\user\.gemini\antigravity-ide\brain\f60bb9cd-7ee0-42e4-83c6-aed06201c81d\.user_uploaded\media_1788300850486.png")

if img_home is not None:
    cv2.imwrite(r"images\about-img.jpg", img_home, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print("Saved images/about-img.jpg for Home Page (Desk with Laptop)!")

if img_about is not None:
    cv2.imwrite(r"images\about-story.jpg", img_about, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print("Saved images/about-story.jpg for About Page (Stone Wall & Tree Table)!")
