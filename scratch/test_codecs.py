import cv2

codecs = ['mp4v', 'avc1', 'H264', 'XVID']
for c in codecs:
    fourcc = cv2.VideoWriter_fourcc(*c)
    out = cv2.VideoWriter(rf"c:\Users\user\Desktop\verolite\scratch\test_{c}.mp4", fourcc, 25.0, (1920, 1080))
    print(f"Codec {c}: isOpened = {out.isOpened()}")
    if out.isOpened():
        # write 1 blank frame
        import numpy as np
        out.write(np.zeros((1080, 1920, 3), dtype=np.uint8))
        out.release()
