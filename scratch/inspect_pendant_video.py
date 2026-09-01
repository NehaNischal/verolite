import cv2

video_path = r"Pendant_light_product_video_202609020317.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Cannot open video file")
else:
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = count / fps if fps > 0 else 0
    print(f"Video specs: {w}x{h}, FPS: {fps}, Frames: {count}, Duration: {duration:.2f}s")
    
    # Save first frame as hero poster poster="hero.jpg"
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("hero.jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        print("Updated hero.jpg with first frame of pendant light video!")
    cap.release()
