import cv2

video_path = r"Pendant_light_product_video_202609020317.mp4"
cap = cv2.VideoCapture(video_path)

frames_to_save = [0, 30, 60, 90, 120, 150, 180, 210, 239]
for f_idx in frames_to_save:
    cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"scratch/pendant_frame_{f_idx}.jpg", frame)

cap.release()
print("Saved sample frames!")
