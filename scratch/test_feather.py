import cv2
import numpy as np

cap = cv2.VideoCapture(r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, 223)
ret, frame = cap.read()
cap.release()

# Let's inspect brightness across Y
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
y_profile = np.mean(gray, axis=1)

# Find where the bright ring is
# Ring is bright (> 50)
bright_y = np.where(y_profile > 30)[0]
print("Bright Y range:", bright_y[0], "to", bright_y[-1])

# In 720x900 frame:
# Chandelier ring is around y=180 to y=360 (center ~ 270)
# Text "GIRO..." is around y=620 to y=750

# If we want the chandelier ring to be vertically centered on a 1080p canvas:
# Target Y center on 1080p canvas is 540 (or 500 for a luxury chandelier suspended look).
# If we scale frame by 1.2x (or 1.0x or 1.1x):
# Let's say scale = 1.0 -> frame is 720x900.
# If ring center in original is y=270, and we want ring center at y=480 on 1080 canvas:
# We shift frame Y offset to: y_offset = 480 - 270 = 210.
# Top of frame will be at y = 210.
# Bottom of frame will be at y = 210 + 900 = 1110 (just slightly off screen at bottom).
# Or scale = 0.95 -> 684x855, ring center at y=256. Shift y_offset = 480 - 256 = 224.

# Let's test seamless text removal:
# Inpainting or background interpolation for y from 580 to 800:
# The background around y=550 has color ~ [12, 10, 14]. At y=850 color ~ [25, 20, 30].
# We can do a smooth vertical gradient fill in the text region (y=580 to 780), perfectly matching top and bottom background!

text_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
text_mask[600:770, :] = 255
inpainted = cv2.inpaint(frame, text_mask, 5, cv2.INPAINT_TELEA)

# Let's also feather the left and right edges (and top/bottom if needed) of the frame
# so it seamlessly fades into dark
w_fade = 60
alpha_x = np.ones(frame.shape[1], dtype=np.float32)
alpha_x[:w_fade] = np.linspace(0, 1, w_fade)
alpha_x[-w_fade:] = np.linspace(1, 0, w_fade)

alpha_y = np.ones(frame.shape[0], dtype=np.float32)
h_fade = 40
alpha_y[:h_fade] = np.linspace(0, 1, h_fade)
alpha_y[-h_fade:] = np.linspace(1, 0, h_fade)

alpha_2d = np.outer(alpha_y, alpha_x)[:, :, np.newaxis]

blended_frame = (inpainted.astype(np.float32) * alpha_2d).astype(np.uint8)

# Now place onto 1920x1080 canvas
# Test various placements:
# Placement 1: Centered horizontally & chandelier at ideal height
canvas1 = np.zeros((1080, 1920, 3), dtype=np.uint8)
# Chandelier ring center at Y=460, X=1350 (Right side, leaving room for hero text on left)
scale = 1.05
fh, fw = int(frame.shape[0] * scale), int(frame.shape[1] * scale)
scaled_f = cv2.resize(blended_frame, (fw, fh))

# Placement right:
x_off = 1920 - fw - 80
y_off = 100 # ring will be at y = 100 + 270*1.05 = 383px

# Clip bounds
y1, y2 = max(0, y_off), min(1080, y_off + fh)
x1, x2 = max(0, x_off), min(1920, x_off + fw)
fy1, fy2 = max(0, -y_off), min(fh, 1080 - y_off)
fx1, fx2 = max(0, -x_off), min(fw, 1920 - x_off)

canvas1[y1:y2, x1:x2] = scaled_f[fy1:fy2, fx1:fx2]
cv2.imwrite(r"c:\Users\user\Desktop\verolite\scratch\test_compose\test_perfect_right.jpg", canvas1)

# Placement 2: Centered full-width
canvas2 = np.zeros((1080, 1920, 3), dtype=np.uint8)
x_off2 = (1920 - fw) // 2
canvas2[y1:y2, x_off2:x_off2+fw] = scaled_f[fy1:fy2, fx1:fx2]
cv2.imwrite(r"c:\Users\user\Desktop\verolite\scratch\test_compose\test_perfect_center.jpg", canvas2)

print("Saved test_perfect_right.jpg and test_perfect_center.jpg")
