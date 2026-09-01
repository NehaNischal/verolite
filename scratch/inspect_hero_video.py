import cv2

cap = cv2.VideoCapture(r"c:\Users\user\Desktop\verolite\hero-video.mp4")
ret, frame = cap.read()
if ret:
    cv2.imwrite(r"c:\Users\user\Desktop\verolite\scratch\hero_video_frame.jpg", frame)
    print("Saved hero_video_frame.jpg")
cap.release()
