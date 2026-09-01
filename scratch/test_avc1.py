import cv2
import os

# Set dll directory so opencv can find openh264
os.add_dll_directory(r"c:\Users\user\Desktop\verolite")
fourcc = cv2.VideoWriter_fourcc(*'avc1')
out = cv2.VideoWriter(r"c:\Users\user\Desktop\verolite\scratch\test_h264.mp4", fourcc, 25.0, (1920, 1080))
print("avc1 isOpened:", out.isOpened())
if out.isOpened():
    import numpy as np
    for _ in range(25):
        out.write(np.zeros((1080, 1920, 3), dtype=np.uint8))
    out.release()
    print("Test video written successfully!")
