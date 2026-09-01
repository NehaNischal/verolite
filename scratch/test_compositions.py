import cv2
import numpy as np
import os

video_path = r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4"
cap = cv2.VideoCapture(video_path)

# Let's inspect frames 150, 186, 220, 240
# Original size: 720x900
# Let's see what happens if we create 1920x1080 canvas with pure dark background
# and place the video on the right or center.

os.makedirs(r"c:\Users\user\Desktop\verolite\scratch\test_compose", exist_ok=True)

cap.set(cv2.CAP_PROP_POS_FRAMES, 223)
ret, frame = cap.read()

if ret:
    # frame is 900 height x 720 width
    h, w, _ = frame.shape
    
    # Test 1: Center scaled to 1080 height
    # Scale 720x900 -> height 1080, width = 720 * (1080/900) = 864
    scaled = cv2.resize(frame, (int(w * 1080 / h), 1080))
    sw = scaled.shape[1] # 864
    
    # Test 1a: Centered on 1920x1080 black canvas
    canvas_center = np.zeros((1080, 1920, 3), dtype=np.uint8)
    x_offset = (1920 - sw) // 2
    canvas_center[:, x_offset:x_offset+sw] = scaled
    cv2.imwrite(r"c:\Users\user\Desktop\verolite\scratch\test_compose\test_centered.jpg", canvas_center)
    
    # Test 1b: Right-aligned / right-centered (so left side has space for hero title)
    # Right side: e.g. x_offset = 1920 - sw - 50 = 1006
    canvas_right = np.zeros((1080, 1920, 3), dtype=np.uint8)
    x_offset_right = 1920 - sw - 100
    canvas_right[:, x_offset_right:x_offset_right+sw] = scaled
    cv2.imwrite(r"c:\Users\user\Desktop\verolite\scratch\test_compose\test_right.jpg", canvas_right)
    
    # Test 1c: Text masked (the "GIRO Circular elegance" text is in the lower portion)
    # Let's find where the text is: y from ~600 to 760 in the 900h frame
    # We can mask out the text in the lower half with pure black (since background is black)
    frame_notext = frame.copy()
    frame_notext[550:800, :] = 0  # Black out GIRO text
    scaled_notext = cv2.resize(frame_notext, (int(w * 1080 / h), 1080))
    
    canvas_notext_center = np.zeros((1080, 1920, 3), dtype=np.uint8)
    canvas_notext_center[:, x_offset:x_offset+sw] = scaled_notext
    cv2.imwrite(r"c:\Users\user\Desktop\verolite\scratch\test_compose\test_notext_center.jpg", canvas_notext_center)

    canvas_notext_right = np.zeros((1080, 1920, 3), dtype=np.uint8)
    canvas_notext_right[:, x_offset_right:x_offset_right+sw] = scaled_notext
    cv2.imwrite(r"c:\Users\user\Desktop\verolite\scratch\test_compose\test_notext_right.jpg", canvas_notext_right)

cap.release()
print("Test compositions saved!")
